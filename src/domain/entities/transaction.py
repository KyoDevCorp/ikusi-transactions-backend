from dataclasses import dataclass
from datetime import datetime

@dataclass
class Transaction:
    id: int
    user_id: int
    amount: float
    concept: str
    created_at: datetime