from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Tuple

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
    geo_file: Path = Path("microstrip.geo")
    pro_file: Path = Path("microstrip.pro")
    resolutions: Tuple[str] = ("EleSta_v",)
    post_process_ops: Tuple[str] = ("Map", "Cut")

    def __init__(self, cfg: MicrostripCfg, experiment_output_dir: Path):
        super().__init__(cfg, experiment_output_dir)

    def run(self):
        # if needed generate mesh files using gmsh
        mesh_file = self.getdp_cli.generate_mesh(
            self.experiment_output_dir / self.geo_file
        )

        # run getdp solver
        for resolution in self.resolutions:
            self.getdp_cli.run_solver(
                resolution=resolution,
                pro_file=self.experiment_output_dir / self.pro_file,
            )

        # run post processing
        for post_process_op in self.post_process_ops:
            self.getdp_cli.run_post(
                self.experiment_output_dir / self.pro_file,
                post_process_op,
            )

        # convert post processing to vtk
        self.reader.read_experiment(self.experiment_output_dir)

        mesh = self.reader.create_pyvista_mesh()
        self.reader.export_to_vtk(
            self.experiment_output_dir / f"{self.cfg.name}.vtk",
            res_filepath=self.experiment_output_dir / f"{self.cfg.name}.res",
        )
