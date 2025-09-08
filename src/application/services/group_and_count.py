from collections import defaultdict
from domain.entities.transaction import Transaction

class GroupTransactionsByConceptUseCase:
    def __init__(self, transactions: list[Transaction]):
        self.transactions = transactions

    def execute(self) -> dict:
        grouped = defaultdict(list)
        totals = defaultdict(float)

        for txn in self.transactions:
            grouped[txn.concept].append(txn)
            totals[txn.concept] += txn.amount

        return {
            "grouped_by_concept": {
                concept: [
                    {
                        "id": t.id,
                        "user_id": t.user_id,
                        "amount": t.amount,
                        "created_at": t.created_at.isoformat()
                    }
                    for t in txns
                ]
                for concept, txns in grouped.items()
            },
            "totals_by_concept": dict(totals),
            "total_transactions": len(self.transactions),
            "overall_total": sum(totals.values())
        }