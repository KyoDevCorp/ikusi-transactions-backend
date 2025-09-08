from abc import ABC, abstractmethod
from typing import List
from domain.entities.transaction import Transaction

class TransactionRepository(ABC):
    @abstractmethod
    def create(self, transaction: Transaction) -> Transaction:
        pass

    @abstractmethod
    def get_by_user_id(self, user_id: int) -> List[Transaction]:
        pass