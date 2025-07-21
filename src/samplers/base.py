from abc import ABC, abstractmethod
from dataclasses import dataclass

import numpy as np


@dataclass
class SamplerBaseCfg:
    sampler: str


@dataclass
class Sampler(ABC):
    cfg: SamplerBaseCfg

    def __init__(self, cfg: SamplerBaseCfg):
        self.cfg = cfg

    @abstractmethod
    def sample(self, n_samples: int) -> np.ndarray:
        pass
