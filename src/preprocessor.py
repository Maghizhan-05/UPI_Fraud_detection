import numpy as np

class Preprocessor:
    @staticmethod
    def extract_features(transactions):
        """
        Builds a (N×3) feature array:
          • amount (normalized)
          • inter‑transaction gap (seconds, normalized)
          • hour‑of‑day (0–23, normalized)
        """
        if not transactions:
            return np.empty((0, 3))

        # 1. Amount
        amounts = np.array([t.amount for t in transactions]).reshape(-1, 1)

        # 2. Time gaps
        times = np.array([t.timestamp.timestamp() for t in transactions]).reshape(-1, 1)
        gaps  = np.diff(times, axis=0)
        gaps  = np.vstack((np.array([[0.]]), gaps))  # pad first gap

        # 3. Hour of day
        hours = np.array([t.timestamp.hour for t in transactions]).reshape(-1, 1)

        # Combine into N×3 matrix
        feats = np.hstack((amounts, gaps, hours))

        # Normalize each column
        mean = feats.mean(axis=0)
        std  = feats.std(axis=0)
        std[std == 0] = 1.0
        return (feats - mean) / std

    @staticmethod
    def to_sequences(features, window=5):
        seqs = []
        for i in range(len(features) - window + 1):
            seq = features[i : i + window]
            if seq.shape[0] == window:
                seqs.append(seq)
        return seqs
