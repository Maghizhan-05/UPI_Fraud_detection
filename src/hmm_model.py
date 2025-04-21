import os
import pickle
import random
import numpy as np
from hmmlearn.hmm import GaussianHMM

class HMMModel:
    def __init__(
        self,
        n_states=4,
        sigma_multiplier=2,
        n_iter=20,
        tol=0.01,
        sample_size=1000,
        model_path='model.pkl'
    ):
        self.n_states = n_states
        self.sigma_multiplier = sigma_multiplier
        self.n_iter = n_iter
        self.tol = tol
        self.sample_size = sample_size
        self.model_path = model_path
        self.model = GaussianHMM(
            n_components=self.n_states,
            covariance_type='diag',
            n_iter=self.n_iter,
            tol=self.tol
        )
        self.threshold = None
        self.load()

    def train(self, sequences):
        seqs = [s for s in sequences if s.ndim == 2 and s.shape[0] > 0]
        if not seqs:
            raise ValueError("No valid sequences to train on")
        if len(seqs) > self.sample_size:
            seqs = random.sample(seqs, self.sample_size)
        X = np.vstack(seqs)
        lengths = [len(s) for s in seqs]
        self.model.fit(X, lengths)
        scores = [self.model.score(s) for s in seqs]
        mean, std = np.mean(scores), np.std(scores)
        self.threshold = mean - self.sigma_multiplier * std
        self.save()

    def is_fraud(self, sequence):
        if self.threshold is None:
            raise RuntimeError("Model not trained")
        return self.model.score(sequence) < self.threshold

    def save(self):
        with open(self.model_path, 'wb') as f:
            pickle.dump({'model': self.model, 'threshold': self.threshold}, f)

    def load(self):
        if os.path.exists(self.model_path):
            with open(self.model_path, 'rb') as f:
                data = pickle.load(f)
                self.model = data['model']
                self.threshold = data['threshold']