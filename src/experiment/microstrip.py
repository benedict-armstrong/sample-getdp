from dataclasses import dataclass, field
from pathlib import Path
from typing import List

from src.experiment.types import Experiment, ExperimentCfg
from src.samplers import SamplerCfg


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
    geo_file: Path = Path("microstrip.geo.j2")
    pro_file: Path = Path("microstrip.pro.j2")
    cases: List[str] = field(default_factory=lambda: ["microstrip.case"])
    post_process_ops: List[str] = field(
        default_factory=lambda: ["microstrip.post_process.j2"]
    )

    def __init__(self, cfg: MicrostripCfg, experiment_output_dir: Path):
        super().__init__(cfg, experiment_output_dir)

    def run(self):
        pass
