#!/usr/bin/env python

'''
Stewart Rand 2015
Halifax crime tweets

Download Halifax crime stats and tweet interesting things

Pre-reqs:
sudo pip install twython
'''

import urllib
import datetime
from dateutil import parser
import pymysql as MySQLdb
import twython
import os
import sys
import logging
import filecmp
import shutil
import json
from pyproj import Transformer

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
LOG_DIR = os.path.join(CURRENT_DIR, 'logs')
LOG_FILE = os.path.join(LOG_DIR, 'halicrime.log')

if not os.path.isdir(LOG_DIR):
    os.makedirs(LOG_DIR)

logging.basicConfig(filename=LOG_FILE,
                    format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)

DATA_URL = os.getenv('DATA_URL', 'https://opendata.arcgis.com/datasets/f6921c5b12e64d17b5cd173cafb23677_0.geojson')

TWITTER_CONSUMER_KEY = 'abc'
TWITTER_CONSUMER_SECRET = 'def'
TWITTER_ACCESS_KEY = 'ghi'
TWITTER_ACCESS_SECRET = 'jkl'
RATE_LIMIT = 123

DB_HOST = os.getenv('DB_HOST') or 'localhost'
DB_USERNAME = os.getenv('MYSQL_USER')
DB_PASSWORD = os.getenv('MYSQL_PASSWORD')
DB_NAME = os.getenv('MYSQL_DATABASE')


def get_twitter_api():
    '''Get connection to Twitter API'''
    return twython.Twython(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET,
                           TWITTER_ACCESS_KEY, TWITTER_ACCESS_SECRET)


def get_db_connection():
    '''Get MySQL DB connection '''
    connection = MySQLdb.connect(DB_HOST, DB_USERNAME, DB_PASSWORD, DB_NAME)
    connection.autocommit(True)
    return connection.cursor()


def parse_row(row):
    '''Get list of column values from row of CSV'''
    return row.strip().split(',')


def get_message_format():
    '''Get the longest message format that we can fit within the allotted characters

    '''
    message_format = ''
    return message_format


def load_data():
    '''Download latest CSV file and load any new data into DB'''
    db = get_db_connection()

    # Delete old event file and move current file to prev
    DATA_DIR = os.path.join(CURRENT_DIR, 'data')

    if not os.path.isdir(DATA_DIR):
        os.makedirs(DATA_DIR)

    latest = os.path.join(DATA_DIR, "latest_events.geojson")
    prev = os.path.join(DATA_DIR, "prev_events.geojson")
    if os.path.isfile(prev):
        os.remove(prev)
    if os.path.isfile(latest):
        shutil.move(latest, prev)

    # Download CSV
    print('Downloading latest GEOJSON.')
    with urllib.request.urlopen(DATA_URL) as response, open(latest, "wb") as out_file:
        out_file.write(response.read())

    # Check if new file is same as old
    if os.path.isfile(prev) and filecmp.cmp(latest, prev):
        print('No new data in GEOJSON.')
        logging.info('No new data in GEOJSON.')
        return

    new_events = 0


    # If it has new data, load data into DB
    with open(latest, 'r') as geojson_file:
        data = json.load(geojson_file)

        # @since Sep 13, 2025 this is no longer lat/lng (EPSG:4326), but "EPSG:3857"
        crs = data['crs']['properties']['name']

        transformer = Transformer.from_crs(crs, "EPSG:4326", always_xy=True)

        features = data['features']

        # Parse each row
        for row in features:
            props = row.get('properties', {})
            try:
                print('Examining row:')
                print(props)
                longitude, latitude = row['geometry']['coordinates']
                longitude, latitude = transformer.transform(longitude, latitude)
                print(longitude, latitude)
                event_id = props['evt_rin']
                event_date = get_date_from_string(props['evt_date'])
                street_name = props['location']
                event_type_id = props['rucr']
                event_type_name = props['rucr_ext_d']
            except Exception as e:
                print('Something wrong with this row')
                logging.info('Something wrong with this row: %s', row)
                logging.exception(e)
                continue

            # Check if it's new
            db.execute("""
                       SELECT *
                       FROM `events`
                       WHERE
                        `date` = "%s"
                        AND `event_id` = %s
                        AND `event_type_id` = %s
                       """ % (event_date, event_id, event_type_id))
            if db.rowcount != 0:
                print('Already in DB.')
                continue
            else:
                print('New entry.')
                new_events += 1

            # Insert into DB
            insert_query = """
                           INSERT INTO
                            `events` (`date_added`, `latitude`, `longitude`, `event_id`, `date`, `street_name`, `event_type_id`, `event_type`)
                           VALUES (CURRENT_DATE(), %s, %s, %s, "%s", "%s", %s, "%s")
                           """ % (latitude, longitude, event_id, event_date, street_name,
                                  event_type_id, event_type_name)
            db.execute(insert_query)
    db.close()
    logging.info("Saved %i new events to database." % new_events)


def get_date_from_string(datelike):
    """Tries a few formatting methods to transform a string into a date
    """
    if '/' in datelike:
        # @since May 9, 2020
        dateformat = '%Y/%m/%d'
    elif '-' in datelike:
        # original format
        dateformat = '%Y-%m-%d'
    else:
        # parse it somehow
        # @since Sep 13, 2025
        return parser.parse(datelike).date()

    return datetime.datetime.strptime(datelike[:10], dateformat).date()


def post_tweets():
    '''Tweet events from DB'''
    # Init connections
    db_connection = MySQLdb.connect(DB_HOST, DB_USERNAME, DB_PASSWORD, DB_NAME)
    db_connection.autocommit(True)
    db_dict_cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)

    api = get_twitter_api()

    # Get shortened URL length from Twitter API
    try:
        shortened_url_length = api.get_twitter_configuration()['short_url_length']
        print('Short URL length as per Twitter API is %i.' % shortened_url_length)
    except KeyError:
        shortened_url_length = 25

    tweet_count = 0

    # TODO: Figure out what to tweet

    db_connection.close()


def main():
    '''Execute main program'''

    if len(sys.argv) != 2 or sys.argv[1] not in ['load_data', 'tweet']:
        print('Please supply a function: either load_data or tweet')
        exit()

    function = sys.argv[1]

    if function == 'load_data':
        load_data()
    elif function == 'tweet':
        post_tweets()


if __name__ == "__main__":
    main()
