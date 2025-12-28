from pydantic import BaseModel
from typing import Optional

class CreditInput(BaseModel):
    worker_id: str
    avg_monthly_income: float
    income_stability: float
    active_months_on_platform: int
    tasks_or_delivery_per_month: int
    avg_bank_balance: float
    past_loan: int
    repayment_percentage: float
    missed_emi: int
    income_shock: int

class CreditResponse(BaseModel):
    worker_id: str
    credit_score: float
    loan_status: str
    confidence: str = "97.5%"
