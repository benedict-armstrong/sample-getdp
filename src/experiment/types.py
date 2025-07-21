from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Dict, List, Union

from src.experiment import get_experiment
from src.getdp import render_template
from src.getdp.getdp_cli import GetDPCLI
from src.samplers import sample_context
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

    def __init__(self, cfg: ExperimentCfg, experiment_output_dir: Path):
        self.cfg = cfg
        self.experiment_output_dir = experiment_output_dir
        self.getdp_cli = GetDPCLI()

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

    @abstractmethod
    def run(self):
        # if needed generate mesh files using gmsh
        mesh_file = self.getdp_cli.generate_mesh(self.geo_file)

        # run getdp solver
        self.getdp_cli.run_solver(cases=self.cases, pro_file=self.pro_file)

        # run post processing
        self.getdp_cli.run_post(self.pro_file)

        # convert post processing to vtk
        self.getdp_cli.convert_pos_to_vtk(pos_file=self.pos_file, mesh_file=mesh_file)

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
    def cases(self) -> List[str]:
        pass

    @property
    @abstractmethod
    def post_process_ops(self) -> List[str]:
        pass
