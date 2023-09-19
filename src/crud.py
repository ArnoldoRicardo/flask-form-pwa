from src.db import get_db_connection, return_db_connection


def get_all_expenses():
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        id
        , total
        , date
        , note
    FROM expenses
    """

    cursor.execute(query)
    records = cursor.fetchall()

    return_db_connection(conn)

    return records


def insert_expense(total: float, note: str) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO expenses (total, note)
    VALUES (%s, %s)
    """

    cursor.execute(query, (total, note))
    conn.commit()

    return_db_connection(conn)

    return True
