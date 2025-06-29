from dataclasses import dataclass

import numpy as np

from .base import Sampler


@dataclass
class LogUniform(Sampler):
    min: float
    max: float

    def sample(self, n_samples: int) -> np.ndarray:
        return np.exp(np.random.uniform(np.log(self.min), np.log(self.max), n_samples))
