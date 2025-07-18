import numpy as np

from .base import Sampler, SamplerCfg
from .loguniform import LogUniform
from .normal import Normal
from .uniform import Uniform
from .uniform_discrete import UniformDiscrete
from .sample_context import sample_context

SAMPLER_MAP = {
    "uniform": Uniform,
    "normal": Normal,
    "loguniform": LogUniform,
    "uniform_discrete": UniformDiscrete,
}


def get_sampler(sampler_cfg: SamplerCfg) -> Sampler:
    return SAMPLER_MAP[sampler_cfg.name](sampler_cfg)


def sample_param(param_cfg, n_samples: int) -> np.ndarray:
    sampler = get_sampler(param_cfg.sampler)
    return sampler.sample(n_samples)
