#!/usr/bin/env python3
"""
Example script demonstrating VTK output and visualization with PyVista.
"""

from src.run_experiments import run_all_experiments_and_save_results, load_vtk_results
from src.visualize_vtk import visualize_experiment, compare_experiments


def main():
    """Example usage of VTK output functionality."""

    print("=== VTK Output Example ===\n")

    # 1. Run experiments with VTK output enabled
    print("1. Running experiments with VTK output...")
    run_all_experiments_and_save_results(
        out_dir="out",
    )

    # 2. Load and visualize VTK results
    print("\n2. Loading VTK results...")

    # Get list of experiment directories
    from pathlib import Path

    out_path = Path("out")
    experiment_dirs = [d.name for d in out_path.iterdir() if d.is_dir()]

    if not experiment_dirs:
        print("No experiment directories found. Please run some experiments first.")
        return

    print(f"Found experiments: {experiment_dirs}")

    # 3. Visualize the first experiment
    if experiment_dirs:
        first_exp = experiment_dirs[0]
        print(f"\n3. Visualizing experiment: {first_exp}")

        # Load VTK results
        vtk_results = load_vtk_results(first_exp)

        if vtk_results:
            print(f"Loaded {len(vtk_results)} VTK files:")
            for filename in vtk_results.keys():
                print(f"  - {filename}")

            # Show a quick visualization
            print("\n4. Opening PyVista viewer...")
            visualize_experiment(first_exp)
        else:
            print("No VTK files found. Make sure experiments completed successfully.")

    # 4. Example of comparing multiple experiments
    if len(experiment_dirs) > 1:
        print(f"\n5. Comparing experiments: {experiment_dirs[:2]}")
        try:
            compare_experiments(experiment_dirs[:2], field_name="v")
        except Exception as e:
            print(f"Error in comparison: {e}")

    print("\n=== Example completed ===")


if __name__ == "__main__":
    main()
