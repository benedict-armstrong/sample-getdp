from dataclasses import asdict, dataclass, field
import os
from pathlib import Path
from typing import List
import uuid

from jinja2 import Environment, FileSystemLoader
import yaml

from src.samplers import sample_context
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
    templates: List[str] | None = field(
        default_factory=lambda: ["microstrip.geo.j2", "microstrip.pro.j2"]
    )


class Microstrip(Experiment):
    cfg: MicrostripCfg

    def __init__(self, cfg: ExperimentCfg):
        super().__init__(cfg)

    def sample(self, output_dir: Path, template_dir: Path) -> None:
        os.makedirs(output_dir, exist_ok=True)

        self.experiment_output_dir = output_dir / uuid.uuid4().hex[:8]
        self.experiment_output_dir.mkdir(parents=True, exist_ok=True)

        # Load jinja2 environment
        env = Environment(
            loader=FileSystemLoader(template_dir / self.cfg.name),
            variable_start_string="[[",
            variable_end_string="]]",
        )

        ctx = sample_context(self.cfg.parameters)

        for template_name in self.cfg.templates:
            template = env.get_template(template_name)
            rendered = template.render(asdict(ctx))
            output_name = template_name[:-3]
            output_path = os.path.join(self.experiment_output_dir, output_name)
            with open(output_path, "w") as f:
                f.write(rendered)
        # Save config
        config_path = os.path.join(self.experiment_output_dir, "config.yaml")
        with open(config_path, "w") as f:
            yaml.dump(asdict(ctx), f)

    def run(self):
        pass
