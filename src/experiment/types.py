from dataclasses import dataclass
from typing import Dict

from src.samplers.base import SamplerCfg


@dataclass
class ExperimentCfg:
    name: str
    n_samples: int
    parameters: Dict[str, SamplerCfg]
    directory: str
