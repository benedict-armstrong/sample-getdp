import subprocess
from pathlib import Path

import gmsh
import pyvista as pv


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
            except:
                pass


class GetDPCLI:
    def __init__(self, getdp_path: str = "getdp", gmsh_path: str = "gmsh"):
        self.getdp_path = getdp_path
        self.gmsh_path = gmsh_path

    def generate_mesh(self, geo_file: Path, dim: int = 2) -> Path:
        """Generate a mesh using gmsh from a .geo file."""
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

            print(f"Generated mesh: {msh_file.name}")
            return msh_file

    def run_solver(self, pro_file: Path, case: str = "EleSta_v"):
        """Run getDP solver for the given .pro file and case."""
        subprocess.run(
            [self.getdp_path, str(pro_file.with_suffix("").name), "-solve", case],
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

    def run_post_vtk(
        self,
        pro_file: Path,
        mesh_file: Path,
        pos: str = "Map",
    ):
        """Run getDP post-processing and convert output to VTK format."""
        # First run the normal post-processing
        self.run_post(pro_file, pos)

        # Convert .pos files to VTK format
        pro_dir = pro_file.parent
        for pos_file in pro_dir.glob("*.pos"):
            self.convert_pos_to_vtk(pos_file, mesh_file)

    def convert_pos_to_vtk(self, pos_file: Path, mesh_file: Path):
        vtk_file = pos_file.with_suffix(".vtk")

        with GmshContext() as gmsh:
            # Clear any existing model
            gmsh.model.remove()

            # First open the mesh file to establish the geometry
            gmsh.open(str(mesh_file))

            # Then merge the .pos file to add the solution data
            gmsh.merge(str(pos_file))

            # Write as VTK with solution data
            gmsh.write(str(vtk_file))

            print(
                f"Converted {pos_file.name} to {vtk_file.name} with solution data (Python API)"
            )

    @staticmethod
    def load_vtk_file(vtk_file: Path):
        """Load a VTK file using PyVista and return the mesh/data."""
        try:
            mesh = pv.read(str(vtk_file))
            return mesh
        except Exception as e:
            print(f"Error loading VTK file {vtk_file}: {e}")
            return None
