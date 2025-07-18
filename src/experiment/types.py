from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Dict

from src.samplers.base import SamplerCfg


@dataclass
class ExperimentCfg:
    name: str
    n_samples: int
    parameters: Dict[str, SamplerCfg]


class Experiment(ABC):
    experiment_output_dir: Path

    def __init__(self, cfg: ExperimentCfg):
        self.cfg = cfg

    @abstractmethod
    def sample(self, output_dir: Path) -> None:
        pass

    @abstractmethod
    def run(self):
        pass
