from datetime import date
from typing import Optional

from pydantic import BaseModel


class Expense(BaseModel):
    id: Optional[int] = None
    total: float
    date: date
    note: str
