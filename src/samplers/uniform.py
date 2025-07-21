from dataclasses import dataclass
from typing import Literal

import numpy as np

from .base import Sampler, SamplerBaseCfg


@dataclass
class UniformCfg(SamplerBaseCfg):
    sampler: Literal["uniform"]
    min: float
    max: float


@dataclass
class Uniform(Sampler):
    cfg: UniformCfg

    def sample(self, n_samples: int) -> np.ndarray:
        return np.random.uniform(self.cfg.min, self.cfg.max, n_samples)
