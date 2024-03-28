import os

import psycopg2.extensions
from flask import Flask, json, request
from jinja2 import (Environment, FileSystemBytecodeCache, PackageLoader,
                    select_autoescape)
from psycopg2 import DatabaseError

from app.database import Database

JSONTEXT = psycopg2.extensions.new_type((114,), "JSONTEXT", (lambda v, c: v))
psycopg2.extensions.register_type(JSONTEXT)

PG_USERNAME = os.getenv("PG_USERNAME")
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_HOST = os.getenv("PG_HOST")
PG_DATABASE = os.getenv("PG_DATABASE")
PG_PORT = os.getenv("PG_PORT")

JINJA_CACHE_FOLDER = os.getenv("JINJA_CACHE_FOLDER")

if not os.path.exists(JINJA_CACHE_FOLDER):
    os.makedirs(JINJA_CACHE_FOLDER)
jinja_env = Environment(
    loader=PackageLoader("app"),
    autoescape=select_autoescape(),
    auto_reload=False,
    bytecode_cache=FileSystemBytecodeCache(JINJA_CACHE_FOLDER, '%s.cache')
)

db = Database(PG_HOST, PG_PORT, PG_DATABASE, PG_USERNAME, PG_PASSWORD)
app = Flask(__name__)


@app.route("/v1/account_accrual_history/<int:p_account_id>", methods=["GET"])
def account_accrual_history_v1(p_account_id):
    offset = request.args.get("offset", 0, type=int)
    limit = request.args.get("limit", 200, type=int)

    sql_template = jinja_env.get_template("account_accrual_history_v1.sql")

    params = {
        'p_account_id': p_account_id,
        'offset': offset,
        'limit': limit,
        'base_url': request.base_url
    }

    result = json.dumps([])
    status_code = 200

    try:
        result = db.fetch_scalar(sql_template, params)
    except DatabaseError as err:
        result = json.dumps(str(err))
        status_code = 500

    return app.response_class(response=result, status=status_code, mimetype='application/json')


@app.route("/v1/personal_account_1/", methods=["GET"])
def personal_account_1_v1():
    offset = request.args.get("offset", 0, type=int)
    limit = request.args.get("limit", 200, type=int)

    sql_template = jinja_env.get_template("personal_account_1_v1.sql")
    params = {
        'offset': offset,
        'limit': limit,
        'base_url': request.base_url
    }

    result = json.dumps([])
    status_code = 200

    try:
        result = db.fetch_scalar(sql_template, params)
    except DatabaseError as err:
        result = json.dumps(str(err))
        status_code = 500

    return app.response_class(response=result, status=status_code, mimetype='application/json')
