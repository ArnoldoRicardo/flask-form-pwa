from datetime import date

from pydantic import BaseModel


class Expense(BaseModel):
    id: int
    total: float
    date: date
    note: str
