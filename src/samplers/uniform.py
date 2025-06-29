from dataclasses import dataclass

import numpy as np

from .base import Sampler


@dataclass
class Uniform(Sampler):
    min: float
    max: float

    def sample(self, n_samples: int) -> np.ndarray:
        return np.random.uniform(self.min, self.max, n_samples)
