# halicrime

Automated crime event Twitter feed bot for Halifax, NS

## developing

1. cp .env-example .env
2. update env variables (GOOGLE_API_KEY, MAIL_HOST, etc.)
3. docker-compose up [-d]
4. go to http://localhost:1902

## debugging

#### retrigger entrypoint scripts

`docker-compose restart`

#### follow logs

`docker-compose logs -f`

#### check service status

`docker-compose ps`

#### destroy containers and data

`docker-compose down -v`

#### run commands in container

`docker-compose exec php bash`

#### rebuild docker containers

`docker-compose up -d --build`

or just:

`docker-compose build`

#### run a one-off script in a container

`docker-compose exec php python halicrime.py load_data`

and:

`docker-compose exec php php notifier.php`

## db backup and restoration

#### Backup

`docker-compose exec mysql bash -c 'mysqldump -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" --databases db' > ./docker/db_dump.sql`

#### Restore

##### Option 1:

`docker-compose exec -T mysql bash -c 'mysql -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" --force' < ./docker/db_dump.sql`

##### Option 2:

On a fresh install, have the sql dump as a volume in docker-compose.yml:

`- ./docker/db_dump.sql:/docker-entrypoint-initdb.d/db_dump.sql`
