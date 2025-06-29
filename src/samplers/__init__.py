import numpy as np
from dataclasses import asdict
from .base import Sampler
from .uniform import Uniform
from .normal import Normal
from .loguniform import LogUniform
from .uniform_discrete import UniformDiscrete


SAMPLER_MAP = {
    "uniform": Uniform,
    "normal": Normal,
    "loguniform": LogUniform,
    "uniform_discrete": UniformDiscrete,
}


def get_sampler(sampler_name: str) -> Sampler:
    return SAMPLER_MAP[sampler_name]


def sample_param(param_cfg, n_samples: int) -> np.ndarray:
    sampler_name = param_cfg.sampler
    sampler = SAMPLER_MAP[sampler_name](**asdict(param_cfg))
    return sampler.sample(n_samples)
