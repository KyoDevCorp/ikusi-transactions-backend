# src/infrastructure/repositories.py
from sqlalchemy.orm import Session
from domain.ports.transaction_repository import TransactionRepository
from domain.entities.transaction import Transaction
from .database import TransactionDB

class SQLTransactionRepository(TransactionRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, transaction: Transaction) -> Transaction:
        db_txn = TransactionDB(
            user_id=transaction.user_id,
            amount=transaction.amount,
            concept=transaction.concept,
            created_at=transaction.created_at
        )
        self.session.add(db_txn)
        self.session.commit()
        self.session.refresh(db_txn)

        return Transaction(
            id=db_txn.id,
            user_id=db_txn.user_id,
            amount=db_txn.amount,
            concept=db_txn.concept,
            created_at=db_txn.created_at
        )

    def get_by_user_id(self, user_id: int) -> list[Transaction]:
        db_txns = self.session.query(TransactionDB).filter(TransactionDB.user_id == user_id).all()
        return [
            Transaction(
                id=t.id,
                user_id=t.user_id,
                amount=t.amount,
                concept=t.concept,
                created_at=t.created_at
            )
            for t in db_txns
        ]