from pathlib import Path

from src.experiment.magnetic_forces import MagneticForces
from src.experiment.microstrip import Microstrip
from src.experiment.types import Experiment, ExperimentCfg

EXPERIMENT_MAP = {
    "microstrip": Microstrip,
    "magnetic_forces": MagneticForces,
}


def get_experiment(
    experiment_cfg: ExperimentCfg, experiment_output_dir: Path
) -> Experiment:
    return EXPERIMENT_MAP[experiment_cfg.name](
        cfg=experiment_cfg,
        experiment_output_dir=experiment_output_dir,
    )
