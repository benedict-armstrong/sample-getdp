from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

from src.experiment.factory import get_experiment
from src.getdp.getdp import GetDPReader
from src.getdp.render_template import render_template
from src.getdp.getdp_cli import GetDPCLI
from src.samplers import SamplerCfg, sample_context


@dataclass
class ExperimentCfg:
    name: str
    n_samples: int
    parameters: Dict[str, SamplerCfg]
    templates: List[str] | None


class Experiment(ABC):
    experiment_output_dir: Path

    def __init__(self, cfg: ExperimentCfg, experiment_output_dir: Path):
        self.cfg = cfg
        self.experiment_output_dir = experiment_output_dir
        self.getdp_cli = GetDPCLI()
        self.reader = GetDPReader()

    @staticmethod
    def sample(
        cfg: ExperimentCfg,
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

    # Abstract properties  below

    @property
    @abstractmethod
    def geo_file(self) -> Path:
        pass

    @property
    @abstractmethod
    def pro_file(self) -> Path:
        pass

    @property
    @abstractmethod
    def resolutions(self) -> List[str]:
        pass

    @property
    @abstractmethod
    def post_process_ops(self) -> List[str]:
        pass
