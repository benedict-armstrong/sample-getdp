import json
import subprocess
from pathlib import Path

from .getdp.getdp_cli import GetDPCLI

# Mapping of experiment types to their main geometry and problem files
EXPERIMENT_FILES = {
    "microstrip": {"geo": "microstrip.geo", "pro": "microstrip.pro"},
    "magnetic_forces": {"geo": "magnets.geo", "pro": "magnets.pro"},
}


def get_experiment_type(exp_dir: Path) -> str:
    """
    Determine the experiment type from the config.json file.

    Args:
        exp_dir: Path to the experiment directory

    Returns:
        str: The experiment type, or None if cannot be determined
    """
    config_file = exp_dir / "config.json"
    if not config_file.exists():
        return None

    try:
        with open(config_file, "r") as f:
            config = json.load(f)

        # Check for experiment-specific parameters to determine type
        if "h" in config and "w" in config and "t" in config:
            return "microstrip"
        elif "num_magnets" in config and "infinite_box" in config and "shape" in config:
            return "magnetic_forces"
        else:
            return None

    except (json.JSONDecodeError, KeyError):
        return None


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

        # Determine experiment type
        exp_type = get_experiment_type(exp_dir)
        if exp_type is None:
            print(f"Skipping {exp_dir.name}: Unknown experiment type")
            continue

        if exp_type not in EXPERIMENT_FILES:
            print(f"Skipping {exp_dir.name}: Unsupported experiment type '{exp_type}'")
            continue

        # Get the appropriate file names for this experiment type
        file_config = EXPERIMENT_FILES[exp_type]
        geo_file = exp_dir / file_config["geo"]
        pro_file = exp_dir / file_config["pro"]

        if not geo_file.exists() or not pro_file.exists():
            print(
                f"Skipping {exp_dir.name}: Missing required files ({file_config['geo']} or {file_config['pro']})"
            )
            continue

        print(f"Processing {exp_type} experiment in {exp_dir.name}")

        # Generate mesh with gmsh
        print("  Generating mesh...")
        try:
            mesh_file = getdp.generate_mesh(geo_file)
            print("  Mesh generated successfully")
        except subprocess.CalledProcessError as e:
            print(f"  Error generating mesh: {e}")
            continue

        # Run solver and post-processing
        try:
            print("  Running solver...")
            getdp.run_solver(pro_file)
            print("  Running post-processing...")

            getdp.run_post_vtk(pro_file, mesh_file, "Map")
            getdp.run_post_vtk(pro_file, mesh_file, "Cut")

            print("  Post-processing completed")
        except subprocess.CalledProcessError as e:
            print(f"  Error running getDP: {e}")
            continue

        vtk_files = list(exp_dir.glob("*.vtk"))
        if vtk_files:
            print(f"  Generated VTK files: {[f.name for f in vtk_files]}")


def load_vtk_results(experiment_dir: str):
    """
    Load VTK files for a specific experiment using PyVista.

    Args:
        experiment_dir: Name of the experiment directory

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
