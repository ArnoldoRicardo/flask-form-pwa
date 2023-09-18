import psycopg2
from psycopg2 import pool
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_CONFIG = {
    'dbname': os.environ.get('POSTGRES_DATABASE'),
    'user': os.environ.get('POSTGRES_USER'),
    'password': os.environ.get('POSTGRES_PASSWORD'),
    'host': os.environ.get('POSTGRES_HOST'),
}

connection_pool = pool.SimpleConnectionPool(1, 10, **DATABASE_CONFIG)

def get_db_connection():
    return connection_pool.getconn()

def return_db_connection(conn):
    connection_pool.putconn(conn)

