from src.experiment.magnetic_forces import MagneticForces
from src.experiment.microstrip import Microstrip
from src.experiment.types import Experiment, ExperimentCfg

EXPERIMENT_MAP = {
    "microstrip": Microstrip,
    "magnetic_forces": MagneticForces,
}


def get_experiment(experiment_cfg: ExperimentCfg) -> Experiment:
    return EXPERIMENT_MAP[experiment_cfg.name](experiment_cfg)
