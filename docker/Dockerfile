FROM php:fpm

WORKDIR /app

#
# adds mysql & mail to php
# installs python for halicrime.py
# installs mariadb-server to ping the db before loading data
#
RUN docker-php-ext-install mysqli \
    && apt-get update \
    && apt-get install -y \
    msmtp \
    python \
    python-pip \
    python-dev \
    mariadb-server \
    cron \
    git \
    && rm -rf /var/lib/apt/lists/*

#
# get requirements for python script
#
COPY requirements.txt .
RUN pip install -r requirements.txt

#
# install composer for phpmailer
#
COPY composer.json \
    composer.lock \
    ./
RUN curl https://getcomposer.org/download/1.10.9/composer.phar \
    --output /usr/local/bin/composer \
    && chmod a+x /usr/local/bin/composer \
    && composer install

#
# need entrypoint to setup mail
#
COPY ./docker/docker-entrypoint.sh /usr/local/bin/

#
# copy crontab
#
COPY ./docker/notifier-cron /etc/cron.d
RUN chmod 0644 /etc/cron.d/notifier-cron \
    && crontab /etc/cron.d/notifier-cron

ENTRYPOINT [ "docker-entrypoint.sh" ]
CMD ["php-fpm"]