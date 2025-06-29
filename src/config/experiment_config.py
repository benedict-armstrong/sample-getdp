from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional

from src.samplers import Sampler, get_sampler


@dataclass
class ExperimentConfig:
    n_samples: int
    parameters: Dict[str, Sampler]
    directory: Path


@dataclass
class MainConfig:
    experiment: ExperimentConfig
    output_dir: str = "out"
    template_dir: Optional[Path] = Path("templates")
    # Add other global settings as needed


def dict_to_experiment_config(d: dict) -> ExperimentConfig:
    params = {k: get_sampler(v["sampler"])(**v) for k, v in d["parameters"].items()}
    return ExperimentConfig(
        n_samples=d["n_samples"], parameters=params, directory=d["directory"]
    )


def dict_to_main_config(d: dict) -> MainConfig:
    d["experiment"] = dict_to_experiment_config(d["experiment"])
    return MainConfig(**d)
