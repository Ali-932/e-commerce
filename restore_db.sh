# PostgreSQL connection details
source .env

HOST=$DB_HOST
PORT=$DB_PORT
USER=$DB_USER
DBNAME=$DB_NAME

PGPASSFILE="$HOME/.pgpass"
echo "$HOST:$PORT:$DBNAME:$USER:$DB_PASS" > $PGPASSFILE
chmod 600 $PGPASSFILE

psql -h $HOST -U $USER -d $DBNAME -p $PORT << EOF
  CREATE ROLE postgres WITH LOGIN PASSWORD 'secretpassword';
  GRANT ALL PRIVILEGES ON DATABASE appdatabase TO postgres;
EOF

# Clean up .pgpass file
rm $PGPASSFILE


python manage.py dbrestore --no-input