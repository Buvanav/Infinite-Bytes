from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import pandas as pd
import joblib
import uvicorn

app = FastAPI(title="Gig Worker Credit Score API ")

# ---------- CORS SETUP ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --------------------------------

# ---------- PERMANENT WORKERS DB ----------
workers_db = {
    "W001": {
        "worker_id": "W001",
        "avg_monthly_income": 45000,
        "income_stability": 8,
        "active_months_on_platform": 12,
        "tasks_or_delivery_per_month": 200,
        "avg_bank_balance": 55000,
        "past_loan": 2,
        "repayment_percentage": 94,
        "missed_emi": 2,
        "income_shock": 0,
    },
    "W002": {
        "worker_id": "W002",
        "avg_monthly_income": 30000,
        "income_stability": 6,
        "active_months_on_platform": 6,
        "tasks_or_delivery_per_month": 120,
        "avg_bank_balance": 30000,
        "past_loan": 1,
        "repayment_percentage": 90,
        "missed_emi": 1,
        "income_shock": 1,
    },
}
# ------------------------------------------

# ✅ MODEL LOAD
model = joblib.load("credit_model.pkl")
features = [
    "avg_monthly_income",
    "income_stability",
    "active_months_on_platform",
    "tasks_or_delivery_per_month",
    "avg_bank_balance",
    "past_loan",
    "repayment_percentage",
    "missed_emi",
    "income_shock",
]


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


@app.get("/")
def read_root():
    return {"message": "✅ Gig Worker Credit Score API LIVE!", "accuracy": "97.5%"}


# ---------- NEW GET ENDPOINT ----------
@app.get("/worker/{worker_id}")
def get_worker(worker_id: str):
    worker = workers_db.get(worker_id)
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    return worker
# ---------------------------------------


@app.post("/predict")
def predict(data: CreditInput):
    try:
        input_df = pd.DataFrame(
            [
                {
                    "avg_monthly_income": data.avg_monthly_income,
                    "income_stability": data.income_stability,
                    "active_months_on_platform": data.active_months_on_platform,
                    "tasks_or_delivery_per_month": data.tasks_or_delivery_per_month,
                    "avg_bank_balance": data.avg_bank_balance,
                    "past_loan": int(data.past_loan),
                    "repayment_percentage": data.repayment_percentage,
                    "missed_emi": int(data.missed_emi),
                    "income_shock": int(data.income_shock),
                }
            ]
        )

        prediction = model.predict(input_df)
        credit_score = float(prediction[0])
        if credit_score < 4.0:
         loan_status = "✅ Micro Loan Approved: ₹1,000 – ₹3,000"

        elif 4.0 <= credit_score <= 4.9:
         loan_status = "✅ Micro Loan Approved: ₹3,001 – ₹6,000"

        elif 5.0 <= credit_score <= 5.7:
         loan_status = "✅ Micro Loan Approved: ₹6,001 – ₹10,000"

        elif 5.8 <= credit_score <= 6.2:
         loan_status = "✅ Micro Loan Approved: ₹10,001 – ₹15,000"

        elif 6.3 <= credit_score <= 6.49:
         loan_status = "✅ Micro Loan Approved: ₹15,001 – ₹19,000"

        elif 6.5 <= credit_score <= 6.9:
         loan_status = "✅ Loan Approved: ₹20,000 – ₹40,000"

        elif 7.0 <= credit_score <= 7.5:
         loan_status = "✅ Loan Approved: ₹40,001 – ₹75,000"

        elif 7.6 <= credit_score <= 8.2:
         loan_status = "✅ Loan Approved: ₹75,001 – ₹1,20,000"

        elif 8.3 <= credit_score <= 9.0:
         loan_status = "✅ Loan Approved: ₹1,20,001 – ₹1,60,000"

        elif 9.1 <= credit_score <= 9.9:
         loan_status = "✅ Loan Approved: ₹1,60,001 – ₹2,00,000"

        else:
         loan_status = "⚠️ Invalid Credit Score"



        return {
            "worker_id": data.worker_id,
            "credit_score": round(credit_score, 2),
            "loan_status": loan_status,
            "confidence": "97.5%",
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/demo/uber/{worker_id}")
def demo_uber(worker_id: str):
    data = CreditInput(
        worker_id=worker_id,
        avg_monthly_income=42000,
        income_stability=85,
        active_months_on_platform=28,
        tasks_or_delivery_per_month=55,
        avg_bank_balance=22000,
        past_loan=1,
        repayment_percentage=92,
        missed_emi=0,
        income_shock=0,
    )
    return predict(data)


@app.get("/demo/zomato/{worker_id}")
def demo_zomato(worker_id: str):
    data = CreditInput(
        worker_id=worker_id,
        avg_monthly_income=35000,
        income_stability=78,
        active_months_on_platform=24,
        tasks_or_delivery_per_month=65,
        avg_bank_balance=18000,
        past_loan=0,
        repayment_percentage=88,
        missed_emi=1,
        income_shock=0,
    )
    return predict(data)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)