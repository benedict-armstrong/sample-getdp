from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional, List

from omegaconf import OmegaConf
from src.samplers import Sampler, get_sampler


@dataclass
class ExperimentConfig:
    type: str  # Experiment type (e.g., "microstrip", "magnetic_forces")
    n_samples: int
    parameters: Dict[str, Sampler]
    directory: Path


@dataclass
class MainConfig:
    experiments: List[ExperimentConfig]
    output_dir: str = "out"
    template_dir: Optional[Path] = Path("templates")


def dict_to_experiment_config(d: dict) -> ExperimentConfig:
    """Convert a dictionary to an ExperimentConfig object."""
    params = {k: get_sampler(v["sampler"])(**v) for k, v in d["parameters"].items()}
    return ExperimentConfig(
        type=d["type"],
        n_samples=d["n_samples"],
        parameters=params,
        directory=Path(d["directory"]),
    )


def load_experiment_config(experiment_name: str, config_dir: Path) -> ExperimentConfig:
    """Load a single experiment config by reading the YAML file directly."""
    experiment_file = config_dir / "experiments" / f"{experiment_name}.yaml"

    if not experiment_file.exists():
        raise FileNotFoundError(f"Experiment config file not found: {experiment_file}")

    cfg = OmegaConf.load(experiment_file)
    return dict_to_experiment_config(OmegaConf.to_container(cfg, resolve=True))


def dict_to_main_config(d: dict, config_dir: Path) -> MainConfig:
    """Convert the main config dict to MainConfig, loading experiment configs from separate files."""
    experiments_to_run = d.get("experiments_to_run", [])

    if not experiments_to_run:
        raise ValueError("No experiments specified in 'experiments_to_run' list")

    # Load each experiment config from its separate file
    experiments = []
    for exp_name in experiments_to_run:
        try:
            exp_config = load_experiment_config(exp_name, config_dir)
            experiments.append(exp_config)
        except Exception as e:
            raise ValueError(f"Failed to load experiment config '{exp_name}': {e}")

    return MainConfig(
        experiments=experiments,
        output_dir=d.get("output_dir", "out"),
        template_dir=Path(d.get("template_dir", "templates")),
    )
