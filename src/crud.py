from src.db import db_connection


def get_all_expenses():
    with db_connection() as conn:
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

    return records


def insert_expense(total: float, note: str) -> bool:
    with db_connection() as conn:
        cursor = conn.cursor()

        query = """
        INSERT INTO expenses (total, note)
        VALUES (%s, %s)
        """

        cursor.execute(query, (total, note))
        conn.commit()

    return True
