# src/main.py
from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from infrastructure.adapters.database import SessionLocal, Base, engine
from infrastructure.adapters.repositories import SQLTransactionRepository
from infrastructure.adapters.http_user_client import UserServiceHTTPClient
from application.services.get_transaction_by_userid import GetTransactionsByUserUseCase
from application.services.create_transaction import CreateTransactionUseCase
from application.services.group_and_count import GroupTransactionsByConceptUseCase
from infrastructure.adapters.logging import logger
from pydantic import BaseModel
from typing import List, Optional
import os

app = FastAPI(
    title="Transacciones Service",
    description="Gestión de transacciones asociadas a usuarios autenticados",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

# Dependencia: sesión de DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user_service():
    base_url = os.getenv(
        "USERS_SERVICE_URL",
        "http://localhost:8000"
    )
    return UserServiceHTTPClient(base_url=base_url)

class TransactionCreate(BaseModel):
    amount: float
    concept: str


@app.post("/transactions/", status_code=201)
def create_transaction(
    transaction: TransactionCreate,
    authorization: str = Header(...),
    db: Session = Depends(get_db),
    user_client: UserServiceHTTPClient = Depends(get_user_service)
):
    token = authorization.replace("Bearer ", "")
    logger.info("create_transaction_attempt", token_preview=token[:10] + "...")

    try:
        use_case = CreateTransactionUseCase(SQLTransactionRepository(db), user_client)
        new_txn = use_case.execute(token, transaction.amount, transaction.concept)
        logger.info("transaction_created", transaction_id=new_txn.id, user_id=new_txn.user_id, amount=new_txn.amount)
        return new_txn
    except ValueError as e:
        logger.warn("create_transaction_failed", error=str(e))
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/transactions/me")
def get_my_transactions(
    authorization: str = Header(...),
    db: Session = Depends(get_db),
    user_client: UserServiceHTTPClient = Depends(get_user_service)
):
    token = authorization.replace("Bearer ", "")
    logger.info("fetch_transactions_attempt", token_preview=token[:10] + "...")

    try:
        use_case = GetTransactionsByUserUseCase(SQLTransactionRepository(db), user_client)
        transactions = use_case.execute(token)
        logger.info("transactions_fetched", count=len(transactions))
        return transactions
    except ValueError as e:
        logger.warn("fetch_transactions_failed", error=str(e))
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/transactions/me/analytics")
def get_transaction_analytics(
    authorization: str = Header(...),
    db: Session = Depends(get_db),
    user_client: UserServiceHTTPClient = Depends(get_user_service)
):
    token = authorization.replace("Bearer ", "")
    logger.info("analytics_requested", token_preview=token[:10] + "...")

    try:
        use_case = GetTransactionsByUserUseCase(SQLTransactionRepository(db), user_client)
        transactions = use_case.execute(token)

        analytics = GroupTransactionsByConceptUseCase(transactions)
        result = analytics.execute()

        logger.info("analytics_generated",
                   concepts=len(result["totals_by_concept"]),
                   total_transactions=result["total_transactions"],
                   overall_total=result["overall_total"])

        return result
    except ValueError as e:
        logger.error("analytics_failed", error=str(e))
        raise HTTPException(status_code=400, detail=str(e))