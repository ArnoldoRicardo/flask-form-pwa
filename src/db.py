import logging
from contextlib import contextmanager

from psycopg2 import OperationalError, pool
from psycopg2.extras import RealDictCursor

from src.config import config

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

DATABASE_CONFIG = {
    'dbname': config.POSTGRES_DATABASE,
    'user': config.POSTGRES_USER,
    'password': config.POSTGRES_PASSWORD,
    'host': config.POSTGRES_HOST,
}

connection_pool = pool.SimpleConnectionPool(1, 10, **DATABASE_CONFIG)


def is_connection_valid(conn):
    """Verify if  a connection is valid"""
    try:
        # Execute a very simple statement to check if cursor is still valid
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        return True
    except OperationalError:
        logger.error("Connection is not valid!")
        return False


def get_db_connection():
    """Get a connection from the pool."""
    try:
        conn = connection_pool.getconn()
        conn.cursor_factory = RealDictCursor
        return conn
    except OperationalError:
        logger.error("Connection pool is empty!")
        raise


def return_db_connection(conn):
    """Return a connection to the pool."""
    if not is_connection_valid(conn):
        conn.close()
        conn = get_db_connection()
    connection_pool.putconn(conn)


@contextmanager
def db_connection():
    """Get a connection from the pool."""
    conn = get_db_connection()
    try:
        yield conn
    finally:
        return_db_connection(conn)


def close_connection_pool():
    """Close all connections in the pool."""
    connection_pool.closeall()
