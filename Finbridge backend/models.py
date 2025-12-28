from sqlmodel import SQLModel, Field, create_engine, Session
from typing import Optional
from datetime import datetime

class Worker(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    worker_id: str = Field(index=True, unique=True)
    avg_monthly_income: float
    income_stability: float
    active_months_on_platform: int
    tasks_or_delivery_per_month: int
    avg_bank_balance: float
    past_loan: int
    repayment_percentage: float
    missed_emi: int
    income_shock: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
