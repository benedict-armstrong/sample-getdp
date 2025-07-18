from dataclasses import dataclass
import random

import numpy as np

from .base import Sampler, SamplerCfg


@dataclass
class UniformDiscreteCfg(SamplerCfg):
    values: list[float] | None = None
    min: int | None = None
    max: int | None = None


@dataclass
class UniformDiscrete(Sampler):
    cfg: UniformDiscreteCfg

    def sample(self, n_samples: int) -> np.ndarray:
        if self.cfg.values is not None:
            return np.array([random.choice(self.cfg.values) for _ in range(n_samples)])
        elif self.cfg.min is not None and self.cfg.max is not None:
            return np.random.randint(self.cfg.min, self.cfg.max + 1, n_samples)
        else:
            raise ValueError("Either values or min and max must be provided")
