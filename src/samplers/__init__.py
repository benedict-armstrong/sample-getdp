from .uniform import sample_uniform
from .normal import sample_normal
from .loguniform import sample_loguniform

SAMPLER_MAP = {
    "uniform": sample_uniform,
    "normal": sample_normal,
    "loguniform": sample_loguniform,
}


def sample_param(param_cfg, n_samples):
    sampler_name = param_cfg.sampler
    sampler = SAMPLER_MAP[sampler_name]
    if sampler_name == "uniform":
        return sampler(param_cfg.min, param_cfg.max, n_samples)
    elif sampler_name == "normal":
        return sampler(param_cfg.mean, param_cfg.std, n_samples)
    elif sampler_name == "loguniform":
        return sampler(param_cfg.min, param_cfg.max, n_samples)
    else:
        raise ValueError(f"Unknown sampler: {sampler_name}")
