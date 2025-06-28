from pathlib import Path
from .experiments.getdp_cli import GetDPCLI
import subprocess


def run_all_experiments_and_save_results(
    out_dir: str = "out",
    getdp_path: str = "getdp",
    gmsh_path: str = "gmsh",
):
    """
    Run all experiments in out_dir, generate mesh with gmsh, process .pos files,
    and save numpy arrays to simulations_dir. Optionally save VTK files for PyVista visualization.
    """
    out_path = Path(out_dir)
    getdp = GetDPCLI(getdp_path, gmsh_path)

    for exp_dir in out_path.iterdir():
        if not exp_dir.is_dir():
            continue
        geo_file = exp_dir / "microstrip.geo"
        pro_file = exp_dir / "microstrip.pro"
        if not geo_file.exists() or not pro_file.exists():
            continue

        print(f"Processing experiment in {exp_dir.name}")

        # Generate mesh with gmsh
        print("  Generating mesh...")
        mesh_file = getdp.generate_mesh(geo_file)
        print("  Mesh generated successfully")

        # Run solver and post-processing
        try:
            print("  Running solver...")
            getdp.run_solver(pro_file)
            print("  Running post-processing...")

            getdp.run_post_vtk(pro_file, mesh_file, "Map")
            getdp.run_post_vtk(pro_file, mesh_file, "Cut")

            print("  Post-processing completed")
        except subprocess.CalledProcessError as e:
            print(f"Error running getDP in {exp_dir}: {e}")
            continue

        vtk_files = list(exp_dir.glob("*.vtk"))
        if vtk_files:
            print(f"  Generated VTK files: {[f.name for f in vtk_files]}")


def load_vtk_results(experiment_dir: str):
    """
    Load VTK files for a specific experiment using PyVista.

    Args:
        experiment_dir: Name of the experiment directory
        simulations_dir: Directory containing simulation results

    Returns:
        dict: Dictionary mapping VTK file names to PyVista mesh objects
    """
    exp_path = Path("out") / experiment_dir

    vtk_results = {}

    # Load VTK files directly from experiment directory
    for vtk_file in exp_path.glob("*.vtk"):
        try:
            mesh = GetDPCLI.load_vtk_file(vtk_file)
            if mesh is not None:
                vtk_results[vtk_file.name] = mesh
                print(f"Loaded VTK file: {vtk_file.name}")
        except Exception as e:
            print(f"Error loading {vtk_file}: {e}")

    return vtk_results


if __name__ == "__main__":
    run_all_experiments_and_save_results()
