import subprocess
from pathlib import Path

import gmsh


class GmshContext:
    """Context manager for Gmsh initialization and cleanup."""

    def __init__(self):
        self.initialized = False

    def __enter__(self):
        gmsh.initialize()
        self.initialized = True
        return gmsh

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.initialized:
            try:
                gmsh.finalize()
            except Exception:
                pass


class GetDPCLI:
    def __init__(self, getdp_path: str = "getdp"):
        self.getdp_path = getdp_path

    def generate_mesh(self, geo_file: Path, dim: int = 2) -> Path:
        """
        Generate mesh using gmsh from .geo files.
        """
        msh_file = geo_file.with_suffix(".msh")

        with GmshContext() as gmsh:
            # Clear any existing model
            gmsh.model.remove()

            # Open the geometry file
            gmsh.open(str(geo_file))

            # Generate mesh
            gmsh.model.mesh.generate(dim)

            # Write mesh file
            gmsh.write(str(msh_file))

        return msh_file

    def run_solver(self, resolution: str, pro_file: Path):
        """Run getDP solver for the given .pro file and resolution."""

        subprocess.run(
            [self.getdp_path, str(pro_file.with_suffix("").name), "-solve", resolution],
            cwd=pro_file.parent,
            check=True,
        )

    def run_post(self, pro_file: Path, pos: str = "Map"):
        """Run getDP post-processing for the given .pro file and pos operation."""
        subprocess.run(
            [self.getdp_path, "-v2", str(pro_file.with_suffix("").name), "-pos", pos],
            cwd=pro_file.parent,
            check=True,
        )
