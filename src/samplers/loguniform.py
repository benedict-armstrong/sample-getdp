import numpy as np
from typing import Tuple


def sample_loguniform(low: float, high: float, size: int) -> np.ndarray:
    """
    Sample from a log-uniform distribution between [low, high) with the given size.
    Returns a numpy array of samples.
    """
    return np.exp(np.random.uniform(np.log(low), np.log(high), size))
