import sqlite3
import os
from src.transaction import Transaction

class TransactionDatabase:
    def __init__(self, path: str = 'data/transactions.db'):
        # ensure directory exists
        os.makedirs(os.path.dirname(path), exist_ok=True)
        # connect once per app instance
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self._create_table()

    def _create_table(self):
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS transactions(
                txn_id TEXT PRIMARY KEY,
                upi_id TEXT,
                timestamp TEXT,
                amount REAL,
                location TEXT,
                label TEXT
            )
            """
        )
        self.conn.commit()

    def insert_many(self, txns: list[Transaction]):
        """
        Bulk insert transactions in one commit for performance.
        """
        data = [(
            txn.txn_id,
            txn.upi_id,
            txn.timestamp.isoformat(),
            txn.amount,
            txn.location,
            txn.label,
        ) for txn in txns]
        self.conn.executemany(
            "INSERT OR IGNORE INTO transactions VALUES (?,?,?,?,?,?)",
            data
        )
        self.conn.commit()

    def fetch_all(self) -> list[Transaction]:
        cur = self.conn.execute(
            "SELECT txn_id, upi_id, timestamp, amount, location, label FROM transactions"
        )
        cols = [c[0] for c in cur.description]
        rows = cur.fetchall()
        return [
            Transaction.from_dict(dict(zip(cols, row)))
            for row in rows
        ]

    def fetch_legit_sequences(self) -> list[float]:
        cur = self.conn.execute(
            "SELECT amount FROM transactions WHERE label='legit' ORDER BY timestamp"
        )
        return [row[0] for row in cur.fetchall()]

    def clear(self):
        """
        Delete all transactions; useful for resetting between runs.
        """
        self.conn.execute("DELETE FROM transactions")
        self.conn.commit()