from pydantic import BaseModel
from typing import List


class PredictRequest(BaseModel):
    worker_id: str
    age: float = 28.0
    hours_worked: float = 40.0
    avg_monthly_income: float = 25000.0


class PredictResponse(BaseModel):
    worker_id: str
    credit_score: float
    status: str
    loan_amount: float
    message: str


class WorkerSummary(BaseModel):
    id: str
    name: str
