import os
from contextlib import contextmanager

from dotenv import load_dotenv
from psycopg2 import pool
from psycopg2.extras import DictCursor

load_dotenv()

DATABASE_CONFIG = {
    'dbname': os.environ.get('POSTGRES_DATABASE'),
    'user': os.environ.get('POSTGRES_USER'),
    'password': os.environ.get('POSTGRES_PASSWORD'),
    'host': os.environ.get('POSTGRES_HOST'),
}

connection_pool = pool.SimpleConnectionPool(1, 10, **DATABASE_CONFIG)


def get_db_connection():
    conn = connection_pool.getconn()
    conn.cursor_factory = DictCursor
    return conn


def return_db_connection(conn):
    connection_pool.putconn(conn)


@contextmanager
def db_connection():
    conn = get_db_connection()
    try:
        yield conn
    finally:
        return_db_connection(conn)
