import sys, os
# Add src/ to path so we can import preprocessor.py directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import numpy as np
import pytest
from preprocessor import Preprocessor

def test_to_sequences_basic():
    features = np.array([[1], [2], [3], [4], [5]])
    seqs = Preprocessor.to_sequences(features, window=3)
    assert len(seqs) == 3
    expected = [
        np.array([[1], [2], [3]]),
        np.array([[2], [3], [4]]),
        np.array([[3], [4], [5]])
    ]
    for out, exp in zip(seqs, expected):
        assert np.array_equal(out, exp)

def test_to_sequences_window_too_large():
    features = np.array([[1], [2]])
    seqs = Preprocessor.to_sequences(features, window=5)
    assert seqs == []
