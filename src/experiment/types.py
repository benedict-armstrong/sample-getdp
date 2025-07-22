from abc import ABC
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

from src.experiment.factory import get_experiment
from src.getdp.getdp import GetDPReader
from src.getdp.render_template import render_template
from src.getdp.getdp_cli import GetDPCLI
from src.samplers import SamplerCfg, sample_context


@dataclass
class ExperimentBaseCfg:
    name: str
    n_samples: int
    resolutions: List[str]
    post_process_ops: List[str]
    geo_file: Path | None
    pro_file: Path | None
    templates: List[Path]
    parameters: Dict[str, SamplerCfg]


class Experiment(ABC):
    experiment_output_dir: Path

    def __init__(self, cfg: ExperimentBaseCfg, experiment_output_dir: Path):
        self.cfg = cfg
        self.experiment_output_dir = experiment_output_dir
        self.getdp_cli = GetDPCLI()
        self.reader = GetDPReader()

        # if geo and pro files are not defined use name.pro and name.geo
        if self.cfg.geo_file is None:
            self.cfg.geo_file = Path(f"{self.cfg.name}.geo")
        if self.cfg.pro_file is None:
            self.cfg.pro_file = Path(f"{self.cfg.name}.pro")

    @staticmethod
    def sample(
        cfg: ExperimentBaseCfg,
        output_dir: Path,
        template_dir: Path,
    ) -> "Experiment":
        """
        Takes cfg samples the parameters and returns a concrete Experiment
        """
        context = sample_context(cfg.parameters)

        # render templates
        experiment_output_dir = render_template(
            context=context,
            experiment_name=cfg.name,
            output_dir=output_dir,
            template_dir=template_dir,
        )

        # init concrete experiment
        experiment = get_experiment(
            experiment_cfg=cfg, experiment_output_dir=experiment_output_dir
        )

        # return concrete experiment
        return experiment

    def run(self):
        pass
