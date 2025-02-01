# Synch with aws

run
```shell
python manage.py migrate
python manage.py collectstatic --noinput --clear --no-post-process
python manage.py migrate_to_s3 --bucket mangastore-static --workers 10 --multipart-size 50 --progress-file upload_state.json --prefix media
./restore_db.sh

```