from dataclasses import dataclass
from pathlib import Path

from src.experiment.types import Experiment, ExperimentBaseCfg
from src.samplers import UniformDiscrete


@dataclass
class MagneticForcesParameters:
    num_magnets: UniformDiscrete
    infinite_box: UniformDiscrete
    shape: UniformDiscrete


@dataclass
class MagneticForcesCfg(ExperimentBaseCfg):
    parameters: MagneticForcesParameters


class MagneticForces(Experiment):
    def __init__(self, cfg: ExperimentBaseCfg, experiment_output_dir: Path):
        super().__init__(cfg, experiment_output_dir)

    def run(self):
        pass
