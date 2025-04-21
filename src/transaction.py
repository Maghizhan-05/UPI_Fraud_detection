from dataclasses import dataclass
from datetime import datetime

@dataclass
class Transaction:
    txn_id: str
    upi_id: str
    timestamp: datetime
    amount: float
    location: str
    label: str  # 'fraud' or 'legit'

    @staticmethod
    def from_dict(d: dict) -> "Transaction":
        """
        Create a Transaction from a dict. If 'label' is missing,
        defaults to 'legit' so unlabeled CSVs won't raise KeyError.
        """
        return Transaction(
            txn_id    = d['txn_id'],
            upi_id    = d['upi_id'],
            timestamp = datetime.fromisoformat(d['timestamp']),
            amount    = float(d['amount']),
            location  = d['location'],
            label     = d.get('label', 'legit')
        )