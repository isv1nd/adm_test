#!/bin/bash

./manage.py check_db_connection --max-counter 60 --sleep-interval 1 \
    || { echo >&2 "[CRIT] test_db_connection fails. Aborting"; exit 1; }
./manage.py migrate \
    || { echo >&2 "[CRIT] migrate fails. Aborting"; exit 1; }
./manage.py runserver 0.0.0.0:8000