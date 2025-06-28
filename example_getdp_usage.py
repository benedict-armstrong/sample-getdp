#!/usr/bin/env python3
"""
Example usage of the GetDPReader class to convert GetDP output files to VTK format.
"""

from pathlib import Path
from src.getdp.getdp import GetDPReader
import pyvista as pv


def main():
    # Example output directory (use one of the existing ones)
    output_dir = Path("out/3b2dda3b-9c93-42a9-94fa-b09718ea4d79")

    # Initialize the GetDP reader
    reader = GetDPReader()

    print("=== GetDP to VTK Converter Example ===\n")

    # Read the mesh file
    msh_file = output_dir / "microstrip.msh"
    print(f"Reading mesh file: {msh_file}")
    mesh_data = reader.read_msh_file(msh_file)
    print(
        f"✓ Loaded mesh with {len(mesh_data['nodes'])} nodes and {len(mesh_data['elements'])} elements"
    )

    # Read the preprocessing file
    pre_file = output_dir / "microstrip.pre"
    print(f"\nReading preprocessing file: {pre_file}")
    dof_data = reader.read_pre_file(pre_file)

    # Show detailed DOF information
    print(f"✓ Loaded {len(dof_data['dof_data_blocks'])} DOF data block(s)")
    for i, block in enumerate(dof_data["dof_data_blocks"]):
        print(f"  Block {block['number']}: {len(block['dofs'])} DOFs")
        print(
            f"    Resolution: {block['resolution_number']}, System: {block['system_number']}"
        )
        print(
            f"    Total DOFs: {block['num_any_dof']}, Reduced DOFs: {block['num_dof']}"
        )

        # Count DOF types
        type_counts = {}
        for dof in block["dofs"]:
            type_name = dof["type_name"]
            type_counts[type_name] = type_counts.get(type_name, 0) + 1

        print(f"    DOF types: {dict(type_counts)}")

    # Create PyVista mesh
    print("\nCreating PyVista mesh...")
    mesh = reader.create_pyvista_mesh()
    print(f"✓ Created mesh with {mesh.n_points} points and {mesh.n_cells} cells")

    # Print mesh summary
    print("\n=== Mesh Summary ===")
    summary = reader.get_summary()
    for category, info in summary.items():
        print(f"{category.capitalize()}:")
        for key, value in info.items():
            print(f"  {key}: {value}")

    # Print available data arrays
    print("\n=== Available Data Arrays ===")
    print("Point data arrays:")
    for name in mesh.point_data.keys():
        array = mesh.point_data[name]
        print(f"  {name}: {array.shape} ({array.dtype})")
        print(f"    Range: [{array.min():.6f}, {array.max():.6f}]")

    # Export to VTK format
    output_vtk = "out/microstrip_output.vtk"
    print(f"\nExporting to VTK: {output_vtk}")
    reader.export_to_vtk(output_vtk)
    print(f"✓ Exported to {output_vtk}")


if __name__ == "__main__":
    main()
