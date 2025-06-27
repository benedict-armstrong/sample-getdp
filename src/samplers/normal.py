import numpy as np
from typing import Tuple


def sample_normal(mean: float, std: float, size: int) -> np.ndarray:
    """
    Sample from a normal (Gaussian) distribution with given mean, std, and size.
    Returns a numpy array of samples.
    """
    return np.random.normal(mean, std, size)
