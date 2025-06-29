from dataclasses import dataclass

import numpy as np

from .base import Sampler


@dataclass
class Normal(Sampler):
    mean: float
    std: float

    def sample(self, n_samples: int) -> np.ndarray:
        return np.random.normal(self.mean, self.std, n_samples)
