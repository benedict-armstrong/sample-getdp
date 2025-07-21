import os
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import List

import yaml
from jinja2 import Environment, FileSystemLoader

from src.experiment.types import Experiment, ExperimentCfg
from src.samplers import sample_context
from src.samplers.base import SamplerCfg


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
    templates: List[str] | None = field(
        default_factory=lambda: ["microstrip.geo.j2", "microstrip.pro.j2"]
    )


class Microstrip(Experiment):
    cfg: MicrostripCfg

    def __init__(self, cfg: MicrostripCfg, experiment_output_dir: Path):
        super().__init__(cfg, experiment_output_dir)

    def run(self):
        pass
