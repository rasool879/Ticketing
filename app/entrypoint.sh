#!/bin/sh
python manage.py makemigrations >> /migrations.log
python manage.py migrate >> /migrations.log
exec "$@"
