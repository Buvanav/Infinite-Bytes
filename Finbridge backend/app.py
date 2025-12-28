from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session
import pandas as pd
import os

from database import create_db_and_tables, get_session
from schemas import PredictRequest, PredictResponse, WorkerSummary
from models import Worker

app = FastAPI(title="Finbridge")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- CSV LOAD ----------
data_dir = "demo_data"
transactions = pd.read_csv(os.path.join(data_dir, "transactions.csv"))
kyc = pd.read_csv(os.path.join(data_dir, "kyc_demo.csv"))
income = pd.read_csv(os.path.join(data_dir, "income_history.csv"))
insurance = pd.read_csv(os.path.join(data_dir, "insurance.csv"))
# -------------------------------


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    # Optional: seed workers from KYC into DB once
    # with Session(engine) as session: ...


@app.get("/")
async def root():
    return {
        "status": "Finbridge Backend 2.0 Ready!",
        "workers": int(len(kyc)),
        "transactions": int(len(transactions)),
    }


@app.get("/workers", response_model=list[WorkerSummary])
async def list_workers():
    return [{"id": row.worker_id, "name": row.name} for _, row in kyc.iterrows()]


@app.get("/worker/{worker_id}")
async def get_worker(worker_id: str):
    if worker_id not in kyc.worker_id.values:
        raise HTTPException(status_code=404, detail="Worker not found")
    k = kyc[kyc.worker_id == worker_id].iloc[0]
    ins = insurance[insurance.worker_id == worker_id].iloc[0]
    txns = transactions[transactions.worker_id == worker_id].tail(10)
    inc = income[income.worker_id == worker_id].tail(6)
    return {
        "kyc": k.to_dict(),
        "insurance": ins.to_dict(),
        "transactions": txns.to_dict("records"),
        "income": inc.to_dict("records"),
    }


@app.get("/history/{worker_id}")
async def history(worker_id: str):
    if worker_id not in kyc.worker_id.values:
        raise HTTPException(404, "Worker not found")
    return transactions[transactions.worker_id == worker_id].to_dict("records")


@app.post("/predict", response_model=PredictResponse)
async def predict(request: PredictRequest, session: Session = Depends(get_session)):
    score = round(
        4.0
        + (request.avg_monthly_income / 5000)
        + (request.hours_worked / 50),
        2,
    )
    status = "APPROVED" if score > 6.5 else "REJECTED"

    # Optional: store worker snapshot in DB
    worker = Worker(
        worker_id=request.worker_id,
        name=request.worker_id,  # or look up from kyc
        age=request.age,
        avg_monthly_income=request.avg_monthly_income,
        hours_worked=request.hours_worked,
    )
    session.add(worker)
    session.commit()

    return PredictResponse(
        worker_id=request.worker_id,
        credit_score=score,
        status=status,
        loan_amount=50000 if score > 6.5 else 0,
        message=f"Loan {status.lower()}",
    )
