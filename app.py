from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
import csv
from src.transaction import Transaction
from src.database import TransactionDatabase
from src.preprocessor import Preprocessor
from src.hmm_model import HMMModel

app = Flask(__name__)
app.secret_key = 'change-me'

db = TransactionDatabase()
model = HMMModel()

@app.route('/', methods=['GET','POST'])
def index():
    if request.method=='POST' and 'file' in request.files:
        f = request.files['file']
        reader = csv.DictReader(f.stream.read().decode().splitlines())
        for row in reader:
            txn = Transaction.from_dict(row)
            db.insert(txn)
        flash('✅ Transactions uploaded.')
        return redirect(url_for('index'))
    return render_template('index.html')

@app.route('/train')
def train():
    txns = sorted(db.fetch_all(), key=lambda t: t.timestamp)
    if len(txns) < 5:
        flash('ℹ️ Need at least 5 transactions to train.')
        return redirect(url_for('index'))

    feats = Preprocessor.extract_features(txns)
    seqs  = Preprocessor.to_sequences(feats, window=5)
    model.train(seqs)
    flash('✅ HMM trained. Threshold set dynamically.')
    return redirect(url_for('index'))

@app.route('/api/detect')
def api_detect():
    txns = sorted(db.fetch_all(), key=lambda t: t.timestamp)
    if len(txns) < 5:
        # not enough data
        return jsonify({'alerts': []})
    feats = Preprocessor.extract_features(txns)
    seqs  = Preprocessor.to_sequences(feats, window=5)
    alerts = [txns[i+4].txn_id for i, s in enumerate(seqs) if model.is_fraud(s)]
    return jsonify({'alerts': alerts})

if __name__=='__main__':
    app.run(debug=True)
