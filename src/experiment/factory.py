from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.experiment.types import Experiment, ExperimentCfg


def get_experiment(
    experiment_cfg: "ExperimentCfg", experiment_output_dir: Path
) -> "Experiment":
    # Import here to avoid circular imports
    from src.experiment.magnetic_forces import MagneticForces
    from src.experiment.microstrip import Microstrip

    EXPERIMENT_MAP = {
        "microstrip": Microstrip,
        "magnetic_forces": MagneticForces,
    }

    return EXPERIMENT_MAP[experiment_cfg.name](
        cfg=experiment_cfg,
        experiment_output_dir=experiment_output_dir,
    )
