from contextlib import contextmanager

from dotenv import load_dotenv
from psycopg2 import OperationalError, pool
from psycopg2.extras import DictCursor

from src.config import config

load_dotenv()

DATABASE_CONFIG = {
    'dbname': config.POSTGRES_DATABASE,
    'user': config.POSTGRES_USER,
    'password': config.POSTGRES_PASSWORD,
    'host': config.POSTGRES_HOST,
}

connection_pool = pool.SimpleConnectionPool(1, 10, **DATABASE_CONFIG)


def is_connection_valid(conn):
    """Verifica si la conexión a la base de datos sigue siendo válida."""
    try:
        # Ejecuta una consulta simple para verificar la conexión
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        return True
    except OperationalError:
        return False


def get_db_connection():
    try:
        conn = connection_pool.getconn()
        conn.cursor_factory = DictCursor
        return conn
    except OperationalError:
        print("Error al conectarse a la base de datos")


def return_db_connection(conn):
    if not is_connection_valid(conn):
        conn.close()
        conn = connection_pool.getconn()
    connection_pool.putconn(conn)


@contextmanager
def db_connection():
    conn = get_db_connection()
    try:
        yield conn
    finally:
        return_db_connection(conn)


def close_connection_pool():
    """Cierra todas las conexiones y el pool."""
    connection_pool.closeall()
