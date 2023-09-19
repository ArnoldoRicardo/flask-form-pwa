from typing import List

from src.db import db_connection
from src.schemas import Expense


def get_all_expenses() -> List[Expense]:
    """Get all expenses from the database"""
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
        cursor.close()

    return [Expense(**record) for record in records]


def insert_expense(expense: Expense) -> bool:
    """Insert an expense into the database"""
    with db_connection() as conn:
        cursor = conn.cursor()

        query = """
        INSERT INTO expenses (total, note, date)
        VALUES (%s, %s, %s)
        """

        cursor.execute(query, (expense.total, expense.note, expense.date))
        conn.commit()

    return True
