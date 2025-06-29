from dataclasses import dataclass
import random

import numpy as np

from .base import Sampler


@dataclass
class UniformDiscrete(Sampler):
    values: list[float] | None = None
    min: int | None = None
    max: int | None = None

    def sample(self, n_samples: int) -> np.ndarray:
        if self.values is not None:
            return np.array([random.choice(self.values) for _ in range(n_samples)])
        elif self.min is not None and self.max is not None:
            return np.random.randint(self.min, self.max + 1, n_samples)
        else:
            raise ValueError("Either values or min and max must be provided")
