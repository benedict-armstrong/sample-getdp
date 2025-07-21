from typing import Any, Dict

import numpy as np

from .base import Sampler
from .loguniform import LogUniform, LogUniformCfg
from .normal import Normal, NormalCfg
from .uniform import Uniform, UniformCfg
from .uniform_discrete import UniformDiscrete, UniformDiscreteCfg

SamplerCfg = UniformCfg | NormalCfg | LogUniformCfg | UniformDiscreteCfg

SAMPLER_MAP = {
    "uniform": Uniform,
    "normal": Normal,
    "loguniform": LogUniform,
    "uniform_discrete": UniformDiscrete,
}


def sample_context(parameters: Dict[str, SamplerCfg]) -> Dict[str, Any]:
    context = {}
    for var, sampler_cfg in parameters.items():
        sampler = get_sampler(sampler_cfg=sampler_cfg)
        context[var] = sampler.sample(1)[0]

    return context


def get_sampler(sampler_cfg: SamplerCfg) -> Sampler:
    return SAMPLER_MAP[sampler_cfg.sampler](sampler_cfg)
