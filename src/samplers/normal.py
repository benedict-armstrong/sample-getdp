from dataclasses import dataclass

import numpy as np

from .base import Sampler, SamplerCfg


@dataclass
class NormalCfg(SamplerCfg):
    mean: float
    std: float


@dataclass
class Normal(Sampler):
    cfg: NormalCfg

    def sample(self, n_samples: int) -> np.ndarray:
        return np.random.normal(self.cfg.mean, self.cfg.std, n_samples)
