# Synch with aws

run
```shell
python manage.py migrate
python manage.py collectstatic --noinput --clear --no-post-process
```