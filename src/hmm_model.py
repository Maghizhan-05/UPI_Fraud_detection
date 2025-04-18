from hmmlearn.hmm import GaussianHMM
import numpy as np

class HMMModel:
    def __init__(self, n_states=4, sigma_multiplier=2):
        self.model = GaussianHMM(
            n_components=n_states,
            covariance_type='diag',
            n_iter=100
        )
        self.threshold = None
        self.sigma_multiplier = sigma_multiplier

    def train(self, sequences):
        # filter out any empty or malformed sequences
        seqs = [s for s in sequences if s.ndim==2 and s.shape[0]>0]
        if not seqs:
            raise ValueError("No valid sequences to train on; need at least one full window.")
        
        X = np.vstack(seqs)
        lengths = [len(s) for s in seqs]
        self.model.fit(X, lengths)

        # dynamic threshold: mean(score) - k·std(score)
        scores = [self.model.score(s) for s in seqs]
        mean, std = np.mean(scores), np.std(scores)
        self.threshold = mean - self.sigma_multiplier * std

    def is_fraud(self, sequence):
        if self.threshold is None:
            raise RuntimeError("Model must be trained before detection.")
        if sequence.ndim!=2 or sequence.size==0:
            raise ValueError("Input must be a non-empty 2D array.")
        return self.model.score(sequence) < self.threshold
