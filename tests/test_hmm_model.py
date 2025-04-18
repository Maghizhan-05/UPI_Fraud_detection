import sys, os
# Add src/ to path so we can import hmm_model.py directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import numpy as np
import pytest
from hmm_model import HMMModel

def test_train_and_threshold_set():
    sequences = [np.zeros((5, 2)) for _ in range(10)]
    model = HMMModel(n_states=2, sigma_multiplier=1)
    model.train(sequences)
    assert model.threshold is not None
    assert isinstance(model.threshold, float)

def test_is_fraud_behaviour():
    sequences = [np.zeros((5, 2)) for _ in range(10)]
    model = HMMModel(n_states=2, sigma_multiplier=1)
    model.train(sequences)

    legit_seq = np.zeros((5, 2))
    assert not model.is_fraud(legit_seq)

    anomaly = np.ones((5, 2)) * 1000
    assert model.is_fraud(anomaly)

def test_is_fraud_without_training():
    model = HMMModel()
    seq = np.zeros((5, 2))
    with pytest.raises(RuntimeError):
        model.is_fraud(seq)
