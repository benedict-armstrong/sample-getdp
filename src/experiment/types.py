from abc import ABC
from dataclasses import dataclass
from typing import Dict

from src.samplers.base import SamplerCfg


@dataclass
class ExperimentCfg:
    name: str
    n_samples: int
    parameters: Dict[str, SamplerCfg]
    directory: str


class Experiment(ABC):
    def __init__(self, cfg: ExperimentCfg):
        self.cfg = cfg

    def run(self):
        pass
