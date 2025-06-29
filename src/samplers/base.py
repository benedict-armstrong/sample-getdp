from abc import ABC, abstractmethod
from dataclasses import dataclass

import numpy as np


@dataclass
class Sampler(ABC):
    sampler: str

    @abstractmethod
    def sample(self, n_samples: int) -> np.ndarray:
        pass
