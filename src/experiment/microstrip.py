from dataclasses import dataclass
from pathlib import Path
from typing import TypedDict

from src.experiment.types import Experiment, ExperimentBaseCfg
from src.samplers import SamplerCfg


class MicrostripParameters(TypedDict):
    h: SamplerCfg
    w: SamplerCfg
    t: SamplerCfg
    xBox: SamplerCfg
    yBox: SamplerCfg
    initial_voltage: SamplerCfg


@dataclass
class MicrostripCfg(ExperimentBaseCfg):
    parameters: MicrostripParameters


class Microstrip(Experiment):
    cfg: MicrostripCfg

    def __init__(self, cfg: MicrostripCfg, experiment_output_dir: Path):
        super().__init__(cfg, experiment_output_dir)

    def run(self):
        # if needed generate mesh files using gmsh
        self.getdp_cli.generate_mesh(self.experiment_output_dir / self.cfg.geo_file)

        # run getdp solver
        for resolution in self.cfg.resolutions:
            self.getdp_cli.run_solver(
                resolution=resolution,
                pro_file=self.experiment_output_dir / self.cfg.pro_file,
            )

        # run post processing
        for post_process_op in self.cfg.post_process_ops:
            self.getdp_cli.run_post(
                self.experiment_output_dir / self.cfg.pro_file,
                post_process_op,
            )

        # convert post processing to vtk
        self.reader.read_experiment(
            self.experiment_output_dir,
            solution_name=self.cfg.name,
        )

        self.reader.create_pyvista_mesh()
        self.reader.export_to_vtk(self.experiment_output_dir / f"{self.cfg.name}.vtk")
