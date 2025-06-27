from dataclasses import dataclass, field
from typing import Dict, Literal, Optional, Union


@dataclass
class UniformSamplerConfig:
    sampler: Literal["uniform"]
    min: float
    max: float


@dataclass
class NormalSamplerConfig:
    sampler: Literal["normal"]
    mean: float
    std: float


@dataclass
class LogUniformSamplerConfig:
    sampler: Literal["loguniform"]
    min: float
    max: float


SamplerConfig = Union[
    UniformSamplerConfig, NormalSamplerConfig, LogUniformSamplerConfig
]


@dataclass
class ExperimentConfig:
    n_samples: int
    parameters: Dict[str, SamplerConfig]


@dataclass
class MainConfig:
    experiment: ExperimentConfig
    output_dir: str = "out"
    template_dir: Optional[str] = "templates"
    # Add other global settings as needed


# --- Conversion utilities ---
def dict_to_sampler_config(d: dict) -> SamplerConfig:
    if d["sampler"] == "uniform":
        return UniformSamplerConfig(**d)
    elif d["sampler"] == "normal":
        return NormalSamplerConfig(**d)
    elif d["sampler"] == "loguniform":
        return LogUniformSamplerConfig(**d)
    else:
        raise ValueError(f"Unknown sampler: {d['sampler']}")


def dict_to_experiment_config(d: dict) -> ExperimentConfig:
    params = {k: dict_to_sampler_config(v) for k, v in d["parameters"].items()}
    return ExperimentConfig(n_samples=d["n_samples"], parameters=params)


def dict_to_main_config(d: dict) -> MainConfig:
    exp = dict_to_experiment_config(d["experiment"])
    return MainConfig(
        experiment=exp,
        output_dir=d.get("output_dir", "out"),
        template_dir=d.get("template_dir", "templates"),
    )
