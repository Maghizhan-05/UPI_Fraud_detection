#!/usr/bin/env python3
import os
import uuid
import random
import argparse
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

def generate_transactions(n, fraud_rate):
    """
    Generate n synthetic UPI transactions with given fraud_rate.
    Returns a pandas DataFrame.
    """
    banks     = ['icici', 'hdfc', 'axis', 'sbi', 'pnb', 'kotak']
    locations = ['Chennai','Mumbai','Delhi','Bengaluru','Kolkata','Hyderabad','Pune','Noida']
    txn_types = ['Peer-to-Peer','Merchant-Payment','Bill-Payment','Recharge']
    devices   = ['Android','iOS','Web']
    
    start = datetime.now() - timedelta(days=30)
    rows = []
    for _ in range(n):
        ts = start + timedelta(minutes=random.randint(0, 30*24*60))
        row = {
            'txn_id':           str(uuid.uuid4()),
            'upi_id':           f"user{random.randint(1,5000)}@{random.choice(banks)}",
            'timestamp':        ts.isoformat(),
            'amount':           round(np.random.lognormal(mean=4, sigma=1), 2),
            'location':         random.choice(locations),
            'transaction_type': random.choice(txn_types),
            'device':           random.choice(devices),
            'ip_address':       f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}",
            'label':            'fraud' if random.random() < fraud_rate else 'legit'
        }
        rows.append(row)
    return pd.DataFrame(rows)

def main():
    p = argparse.ArgumentParser(
        description="Generate synthetic UPI transactions CSV"
    )
    p.add_argument(
        "--rows", type=int, required=True,
        help="Number of transactions to generate"
    )
    p.add_argument(
        "--fraud_rate", type=float, default=0.05,
        help="Fraction of transactions labeled 'fraud' (0–1)"
    )
    p.add_argument(
        "--output", type=str, default="data/synthetic_transactions.csv",
        help="Path to output CSV file"
    )
    args = p.parse_args()

    # ensure output directory exists
    out_dir = os.path.dirname(args.output)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    # generate and save
    df = generate_transactions(args.rows, args.fraud_rate)
    df.to_csv(args.output, index=False)
    print(f"Generated {args.rows} transactions ({args.fraud_rate*100:.1f}% fraud)")
    print(f"Saved to: {args.output}")

if __name__ == "__main__":
    main()
