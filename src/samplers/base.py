from abc import ABC, abstractmethod
from dataclasses import dataclass

import numpy as np


@dataclass
class SamplerCfg:
    sampler: str


@dataclass
class Sampler(ABC):
    cfg: SamplerCfg

    def __init__(self, cfg: SamplerCfg):
        self.cfg = cfg

    @abstractmethod
    def sample(self, n_samples: int) -> np.ndarray:
        pass
