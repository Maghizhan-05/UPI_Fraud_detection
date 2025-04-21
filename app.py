from flask import Flask, render_template, request, jsonify
import csv
import os
from src.transaction import Transaction
from src.database import TransactionDatabase
from src.preprocessor import Preprocessor
from src.hmm_model import HMMModel

app = Flask(__name__)
app.secret_key = os.urandom(16)

db = TransactionDatabase()
model = HMMModel(
    n_states=4, sigma_multiplier=2,
    n_iter=20, tol=0.01, sample_size=1000,
    model_path='model.pkl'
)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/api/upload', methods=['POST'])
def api_upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    f = request.files['file']
    reader = csv.DictReader(f.stream.read().decode().splitlines())
    txns = [Transaction.from_dict(row) for row in reader]
    db.clear()  # optional: reset on new upload
    db.insert_many(txns)
    return jsonify({'status':'uploaded'})

@app.route('/api/train', methods=['POST'])
def api_train():
    txns = sorted(db.fetch_all(), key=lambda t: t.timestamp)
    if len(txns) < 5:
        return jsonify({'error': 'Need at least 5 transactions'}), 400
    feats = Preprocessor.extract_features(txns)
    seqs  = Preprocessor.to_sequences(feats, window=5)
    model.train(seqs)
    return jsonify({'status': 'trained'})

@app.route('/api/detect', methods=['GET'])
def api_detect():
    if model.threshold is None:
        return jsonify({'error': 'Model not trained', 'alerts': []}), 400
    txns = sorted(db.fetch_all(), key=lambda t: t.timestamp)
    feats = Preprocessor.extract_features(txns)
    seqs  = Preprocessor.to_sequences(feats, window=5)
    alerts = [txns[i+4].txn_id for i, s in enumerate(seqs) if model.is_fraud(s)]
    return jsonify({'status':'detected','alerts': alerts})

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)