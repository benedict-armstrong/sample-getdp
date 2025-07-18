from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, TYPE_CHECKING, Union

from src.samplers.base import SamplerCfg

if TYPE_CHECKING:
    from src.experiment.magnetic_forces import MagneticForcesParameters
    from src.experiment.microstrip import MicrostripParameters

# Move ParameterCfgs here to break circular import
ParameterCfgs = Union["MagneticForcesParameters", "MicrostripParameters"]


@dataclass
class ExperimentCfg:
    name: str
    n_samples: int
    parameters: Dict[str, SamplerCfg]
    templates: List[str] | None


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
