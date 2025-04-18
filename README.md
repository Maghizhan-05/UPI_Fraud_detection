# UPI Fraud Detection using Hidden Markov Model (HMM)

A Flask‑based web application and Python library that uses an unsupervised Hidden Markov Model to detect anomalous (potentially fraudulent) UPI transactions. Includes synthetic dataset generators, feature‑engineering pipeline, model training/evaluation scripts, and a slick UI with animated transitions.

---

## 🔍 Project Overview

- **Goal**: Learn “normal” transaction behavior from legitimate data and flag anomalous sequences as fraud.
- **Core Tech**: Python, Flask, `hmmlearn`, pandas, NumPy, scikit‑learn.
- **Key Features**:
  - Multi‑feature extraction (amount, time‑gap, hour‑of‑day, etc.)
  - Dynamic HMM thresholding (mean – σ×k)
  - Automated hyperparameter grid‑search for best F1
  - Synthetic dataset generators (various sizes and fraud rates)
  - RESTful detection API + animated single‑page UI

---


---

## 🚀 Quick Start

### 1. Clone & install

```bash
git clone https://github.com/your‑username/upi_fraud_detection.git
cd upi_fraud_detection

python3 -m venv venv
source venv/bin/activate          # Windows: .\venv\Scripts\Activate
pip install --upgrade pip
pip install -r requirements.txt

python - <<'PYCODE'
from src.database import TransactionDatabase
TransactionDatabase()  # creates data/transactions.db
PYCODE

pytest --maxfail=1 --disable-warnings -q

python app.py

