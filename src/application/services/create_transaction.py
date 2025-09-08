from domain.ports.transaction_repository import TransactionRepository
from domain.services.user_service import UserServiceClient
from domain.entities.transaction import Transaction
from datetime import datetime, timezone

class CreateTransactionUseCase:
    def __init__(self, repo: TransactionRepository, user_client: UserServiceClient):
        self.repo = repo
        self.user_client = user_client

    def execute(self, token: str, amount: float, concept: str) -> Transaction:
        user_data = self.user_client.get_user_by_token(token)
        user_id = user_data["user_id"]

        transaction = Transaction(
            id=0,
            user_id=user_id,
            amount=amount,
            concept=concept,
            created_at=datetime.now(timezone.utc)
        )

        return self.repo.create(transaction)