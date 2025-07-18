from dataclasses import dataclass

import numpy as np

from .base import Sampler, SamplerCfg


@dataclass
class UniformCfg(SamplerCfg):
    min: float
    max: float


@dataclass
class Uniform(Sampler):
    cfg: UniformCfg

    def sample(self, n_samples: int) -> np.ndarray:
        return np.random.uniform(self.cfg.min, self.cfg.max, n_samples)
