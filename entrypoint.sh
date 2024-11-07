#!/bin/sh

until cd /app
do
    echo "Waiting for server volume to be ready .."
done

cd /app

export DJANGO_SUPERUSER_USERNAME=a
export DJANGO_SUPERUSER_EMAIL=a@a.com
export DJANGO_SUPERUSER_PASSWORD=a

# Django commands
DjangoManage () {
  python manage.py makemigrations
  python manage.py migrate
  python manage.py createsuperuser --noinput 2> /dev/null
}

# If not arguments supplied then just run server
if [ $# -eq 0 ]; then
  DjangoManage
  python manage.py runserver 0.0.0.0:8000

# Else, preepare django and run whatever argument supplied
else
  DjangoManage
  exec $@

fi


