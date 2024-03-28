#! /usr/bin/env sh

postgres_ready() {
    python3 <<END
import sys
import psycopg2
from os import environ

def get_env(key, default=None):
    val = environ.get(key, default)
    if val == 'True':
        val = True
    elif val == 'False':
        val = False
    return val

try:
    dbname = get_env('PG_DATABASE')
    user = get_env('PG_USERNAME')
    password = get_env('PG_PASSWORD')
    host = get_env('PG_HOST')
    port = get_env('PG_PORT')
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

until postgres_ready; do
    echo >&2 "Postgres is unavailable - sleeping"
    sleep 1
done

echo >&2 "Postgres is up - continuing..."

echo >&2 "Starting uwsgi..."
exec uwsgi ./app/app.ini --wsgi-file app.py
