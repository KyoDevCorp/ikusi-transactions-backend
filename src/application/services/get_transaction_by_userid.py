from domain.ports.transaction_repository import TransactionRepository
from domain.services.user_service import UserServiceClient
from domain.entities.transaction import Transaction
from typing import List

class GetTransactionsByUserUseCase:
    def __init__(self, repo: TransactionRepository, user_client: UserServiceClient):
        self.repo = repo
        self.user_client = user_client

    def execute(self, token: str) -> List[Transaction]:
        user_data = self.user_client.get_user_by_token(token)
        user_id = user_data["user_id"]

        return self.repo.get_by_user_id(user_id)