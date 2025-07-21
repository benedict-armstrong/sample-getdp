from dataclasses import dataclass
from typing import Literal

import numpy as np

from .base import Sampler, SamplerBaseCfg


@dataclass
class NormalCfg(SamplerBaseCfg):
    sampler: Literal["normal"]
    mean: float
    std: float


@dataclass
class Normal(Sampler):
    cfg: NormalCfg

    def sample(self, n_samples: int) -> np.ndarray:
        return np.random.normal(self.cfg.mean, self.cfg.std, n_samples)
