from dataclasses import dataclass
from typing import Literal

import numpy as np

from .base import Sampler, SamplerBaseCfg


@dataclass
class LogUniformCfg(SamplerBaseCfg):
    sampler: Literal["loguniform"]
    min: float
    max: float


@dataclass
class LogUniform(Sampler):
    cfg: LogUniformCfg

    def sample(self, n_samples: int) -> np.ndarray:
        return np.exp(
            np.random.uniform(np.log(self.cfg.min), np.log(self.cfg.max), n_samples)
        )
