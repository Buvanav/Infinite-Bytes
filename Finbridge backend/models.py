from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class Worker(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    worker_id: str = Field(index=True, unique=True)
    name: str
    age: float
    avg_monthly_income: float
    hours_worked: float
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    worker_id: str = Field(index=True)
    amount: float
    category: str
    timestamp: datetime
