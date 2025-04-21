#!/usr/bin/env python3
import argparse, os, sys
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score, classification_report

# ensure project root is on path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.transaction import Transaction
from src.preprocessor import Preprocessor
from src.hmm_model import HMMModel

def load_transactions(path):
    df = pd.read_csv(path)
    txns = []
    for row in df.to_dict(orient='records'):
        d = {
          'txn_id':    row['txn_id'],
          'upi_id':    row['upi_id'],
          'timestamp': row['timestamp'],
          'amount':    row['amount'],
          'location':  row['location'],
          'label':     row['label']
        }
        txns.append(Transaction.from_dict(d))
    return sorted(txns, key=lambda t: t.timestamp)

def evaluate(train_seqs, test_txns, test_seqs, model):
    # true / pred
    y_true = [1 if test_txns[i+4].label == 'fraud' else 0
              for i in range(len(test_seqs))]
    y_pred = [1 if model.is_fraud(s) else 0 for s in test_seqs]

    print(classification_report(y_true, y_pred, target_names=['Legit','Fraud']))
    print(f"Accuracy  : {accuracy_score(y_true,y_pred):.3f}")
    print(f"Precision : {precision_score(y_true,y_pred):.3f}")
    print(f"Recall    : {recall_score(y_true,y_pred):.3f}")
    print(f"F1 Score  : {f1_score(y_true,y_pred):.3f}")

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--train',      required=True)
    p.add_argument('--test',       required=True)
    p.add_argument('--window',     type=int,   default=5)
    p.add_argument('--states',     type=int,   default=4)
    p.add_argument('--sigma',      type=float, default=2.0)
    p.add_argument('--grid',       action='store_true',
                   help='Grid search over --states-list and --sigma-list')
    p.add_argument('--states-list',nargs='+',type=int,   default=[2,4,6])
    p.add_argument('--sigma-list', nargs='+',type=float, default=[1.5,2.0,2.5,3.0])
    args = p.parse_args()

    # Load & prepare
    train_txns = load_transactions(args.train)
    feats_train = Preprocessor.extract_features(train_txns)
    seqs_train  = Preprocessor.to_sequences(feats_train, window=args.window)

    test_txns  = load_transactions(args.test)
    feats_test = Preprocessor.extract_features(test_txns)
    seqs_test  = Preprocessor.to_sequences(feats_test, window=args.window)

    if args.grid:
        best = {'f1': 0.0}
        for s in args.states_list:
            for σ in args.sigma_list:
                model = HMMModel(n_states=s, sigma_multiplier=σ)
                model.train(seqs_train)
                y_true = [1 if test_txns[i+args.window-1].label=='fraud' else 0
                          for i in range(len(seqs_test))]
                y_pred = [1 if model.is_fraud(seq) else 0 for seq in seqs_test]
                f1 = f1_score(y_true, y_pred)
                if f1 > best['f1']:
                    best = {'states': s, 'sigma': σ, 'f1': f1}
        print(f"→ Best params: n_states={best['states']}, sigma={best['sigma']},  F1={best['f1']:.3f}")
        return

    # Regular evaluation
    model = HMMModel(n_states=args.states, sigma_multiplier=args.sigma)
    model.train(seqs_train)

    print("\n=== Test Set Performance ===")
    evaluate(seqs_train, test_txns, seqs_test, model)

    # Save detailed report
    os.makedirs('results', exist_ok=True)
    scores = [model.model.score(seq) for seq in seqs_test]
    mean, std = np.mean(scores), np.std(scores)
    confidences = [(model.threshold - sc)/std for sc in scores]

    df = pd.DataFrame({
      'txn_id':     [test_txns[i+args.window-1].txn_id for i in range(len(seqs_test))],
      'true_label': [1 if test_txns[i+args.window-1].label=='fraud' else 0 for i in range(len(seqs_test))],
      'pred_label': [1 if model.is_fraud(seq) else 0 for seq in seqs_test],
      'score':      scores,
      'confidence': confidences
    })
    path = 'results/evaluation_report.csv'
    df.to_csv(path, index=False)
    print(f"\nDetailed report: {path}\n")

if __name__=='__main__':
    main()