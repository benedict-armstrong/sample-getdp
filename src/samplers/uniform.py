import numpy as np
from typing import Tuple


def sample_uniform(low: float, high: float, size: int) -> np.ndarray:
    """
    Sample from a uniform distribution in [low, high) with the given size.
    Returns a numpy array of samples.
    """
    return np.random.uniform(low, high, size)
