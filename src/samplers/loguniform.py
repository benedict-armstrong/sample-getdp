from dataclasses import dataclass

import numpy as np

from .base import Sampler, SamplerCfg


@dataclass
class LogUniformCfg(SamplerCfg):
    min: float
    max: float


@dataclass
class LogUniform(Sampler):
    cfg: LogUniformCfg

    def sample(self, n_samples: int) -> np.ndarray:
        return np.exp(
            np.random.uniform(np.log(self.cfg.min), np.log(self.cfg.max), n_samples)
        )
