import sys, os
# Add src/ to path so we can import transaction.py directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import pytest
from datetime import datetime
from transaction import Transaction

def test_from_dict_valid():
    data = {
        'txn_id': 'abc123',
        'upi_id': 'user@bank',
        'timestamp': '2025-04-18T10:30:00',
        'amount': '250.75',
        'location': 'Chennai',
        'label': 'legit'
    }
    txn = Transaction.from_dict(data)
    assert txn.txn_id == 'abc123'
    assert txn.upi_id == 'user@bank'
    assert isinstance(txn.timestamp, datetime)
    assert txn.timestamp == datetime.fromisoformat('2025-04-18T10:30:00')
    assert txn.amount == 250.75
    assert txn.location == 'Chennai'
    assert txn.label == 'legit'

def test_from_dict_missing_key():
    incomplete = {
        'txn_id': 'id',
        # missing 'upi_id'
        'timestamp': '2025-04-18T10:30:00',
        'amount': '100',
        'location': 'Mumbai',
        'label': 'fraud'
    }
    with pytest.raises(KeyError):
        Transaction.from_dict(incomplete)
