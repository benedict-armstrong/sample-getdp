from dataclasses import dataclass
from pathlib import Path

from src.samplers.base import SamplerCfg
from src.experiment.types import Experiment, ExperimentCfg


@dataclass
class MicrostripParameters:
    h: SamplerCfg
    w: SamplerCfg
    t: SamplerCfg
    xBox: SamplerCfg
    yBox: SamplerCfg
    initial_voltage: SamplerCfg


@dataclass
class MicrostripCfg(ExperimentCfg):
    parameters: MicrostripParameters


class Microstrip(Experiment):
    def __init__(self, cfg: ExperimentCfg):
        super().__init__(cfg)

    def sample(self, output_dir: Path) -> None:
        pass

    def run(self):
        pass
