from dataclasses import dataclass
from pathlib import Path

from src.experiment.types import Experiment, ExperimentCfg
from src.samplers import UniformDiscrete


@dataclass
class MagneticForcesParameters:
    num_magnets: UniformDiscrete
    infinite_box: UniformDiscrete
    shape: UniformDiscrete


@dataclass
class MagneticForcesCfg(ExperimentCfg):
    parameters: MagneticForcesParameters


class MagneticForces(Experiment):
    def __init__(self, cfg: ExperimentCfg):
        super().__init__(cfg)

    def run(self):
        pass
