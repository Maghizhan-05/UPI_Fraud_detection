import csv, random, uuid, datetime

def generate(n=1000, fraud_pct=0.05, out='data/synthetic/transactions.csv'):
    headers = ['txn_id','upi_id','timestamp','amount','location','label']
    with open(out,'w',newline='') as f:
        w = csv.writer(f)
        w.writerow(headers)
        for _ in range(n):
            txn_id = str(uuid.uuid4())
            upi = f"user{random.randint(1,100)}@bank"
            ts = datetime.datetime.now() - datetime.timedelta(minutes=random.randint(0,10000))
            amt = round(random.uniform(10,5000),2)
            loc = random.choice(['Chennai','Mumbai','Delhi'])
            label = 'fraud' if random.random()<fraud_pct else 'legit'
            w.writerow([txn_id,upi,ts.isoformat(),amt,loc,label])

if __name__=='__main__':
    generate()
