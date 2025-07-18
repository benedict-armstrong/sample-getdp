from dataclasses import dataclass
from pathlib import Path

from src.samplers import UniformDiscrete
from src.experiment.types import Experiment, ExperimentCfg


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

    def sample(self, output_dir: Path) -> None:
        pass

    def run(self):
        pass
