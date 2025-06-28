import numpy as np
import pyvista as pv
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Union
import re


class GetDPReader:
    """
    A class to read GetDP output files and convert them to usable formats.

    This class can read:
    - .msh files (mesh geometry in Gmsh format)
    - .pre files (preprocessing information about degrees of freedom)
    - .res files (solution data)

    And convert them to VTK format using PyVista.
    """

    def __init__(self):
        self.mesh_data = {}
        self.dof_data = {}
        self.solution_data = {}
        self.mesh = None

    def read_msh_file(self, filepath: Union[str, Path]) -> Dict:
        """
        Read a Gmsh .msh file and extract mesh information.

        Args:
            filepath: Path to the .msh file

        Returns:
            Dictionary containing nodes and elements data
        """
        filepath = Path(filepath)
        if not filepath.exists():
            raise FileNotFoundError(f"MSH file not found: {filepath}")

        mesh_data = {
            "nodes": {},
            "elements": {},
            "physical_names": {},
            "format_info": {},
        }

        with open(filepath, "r") as f:
            content = f.read()

        # Parse mesh format
        format_match = re.search(
            r"\$MeshFormat\n(.*?)\n\$EndMeshFormat", content, re.DOTALL
        )
        if format_match:
            format_line = format_match.group(1).strip()
            parts = format_line.split()
            mesh_data["format_info"] = {
                "version": parts[0],
                "file_type": int(parts[1]),
                "data_size": int(parts[2]),
            }

        # Parse physical names
        phys_match = re.search(
            r"\$PhysicalNames\n(.*?)\n\$EndPhysicalNames", content, re.DOTALL
        )
        if phys_match:
            phys_content = phys_match.group(1).strip().split("\n")
            num_phys = int(phys_content[0])
            for i in range(1, num_phys + 1):
                if i < len(phys_content):
                    parts = phys_content[i].split()
                    dim = int(parts[0])
                    tag = int(parts[1])
                    name = parts[2].strip('"')
                    mesh_data["physical_names"][tag] = {"dimension": dim, "name": name}

        # Parse nodes
        nodes_match = re.search(r"\$Nodes\n(.*?)\n\$EndNodes", content, re.DOTALL)
        if nodes_match:
            nodes_content = nodes_match.group(1).strip().split("\n")

            # Handle different mesh format versions
            if mesh_data["format_info"].get("version", "").startswith("4"):
                # Version 4.x format
                self._parse_nodes_v4(nodes_content, mesh_data)
            else:
                # Legacy format
                self._parse_nodes_legacy(nodes_content, mesh_data)

        # Parse elements
        elements_match = re.search(
            r"\$Elements\n(.*?)\n\$EndElements", content, re.DOTALL
        )
        if elements_match:
            elements_content = elements_match.group(1).strip().split("\n")

            if mesh_data["format_info"].get("version", "").startswith("4"):
                # Version 4.x format
                self._parse_elements_v4(elements_content, mesh_data)
            else:
                # Legacy format
                self._parse_elements_legacy(elements_content, mesh_data)

        self.mesh_data = mesh_data
        return mesh_data

    def _parse_nodes_v4(self, nodes_content: List[str], mesh_data: Dict):
        """Parse nodes in Gmsh format version 4.x"""
        lines = nodes_content
        line_idx = 0

        # First line: numEntityBlocks numNodes minNodeTag maxNodeTag
        header = lines[line_idx].split()
        num_entity_blocks = int(header[0])
        num_nodes = int(header[1])
        line_idx += 1

        nodes = {}

        for block in range(num_entity_blocks):
            # Entity block header: entityDim entityTag parametric numNodesInBlock
            block_header = lines[line_idx].split()
            entity_dim = int(block_header[0])
            entity_tag = int(block_header[1])
            parametric = int(block_header[2])
            num_nodes_in_block = int(block_header[3])
            line_idx += 1

            # Node tags
            node_tags = []
            for i in range(num_nodes_in_block):
                node_tags.append(int(lines[line_idx]))
                line_idx += 1

            # Node coordinates
            for i, tag in enumerate(node_tags):
                coords = lines[line_idx].split()
                nodes[tag] = [float(coords[0]), float(coords[1]), float(coords[2])]
                line_idx += 1

        mesh_data["nodes"] = nodes

    def _parse_nodes_legacy(self, nodes_content: List[str], mesh_data: Dict):
        """Parse nodes in legacy Gmsh format"""
        num_nodes = int(nodes_content[0])
        nodes = {}

        for i in range(1, num_nodes + 1):
            parts = nodes_content[i].split()
            tag = int(parts[0])
            coords = [float(parts[1]), float(parts[2]), float(parts[3])]
            nodes[tag] = coords

        mesh_data["nodes"] = nodes

    def _parse_elements_v4(self, elements_content: List[str], mesh_data: Dict):
        """Parse elements in Gmsh format version 4.x"""
        lines = elements_content
        line_idx = 0

        # First line: numEntityBlocks numElements minElementTag maxElementTag
        header = lines[line_idx].split()
        num_entity_blocks = int(header[0])
        num_elements = int(header[1])
        line_idx += 1

        elements = {}

        for block in range(num_entity_blocks):
            # Entity block header: entityDim entityTag elementType numElementsInBlock
            block_header = lines[line_idx].split()
            entity_dim = int(block_header[0])
            entity_tag = int(block_header[1])
            element_type = int(block_header[2])
            num_elements_in_block = int(block_header[3])
            line_idx += 1

            for i in range(num_elements_in_block):
                parts = lines[line_idx].split()
                elem_tag = int(parts[0])
                node_tags = [int(x) for x in parts[1:]]

                elements[elem_tag] = {
                    "type": element_type,
                    "entity_tag": entity_tag,
                    "nodes": node_tags,
                }
                line_idx += 1

        mesh_data["elements"] = elements

    def _parse_elements_legacy(self, elements_content: List[str], mesh_data: Dict):
        """Parse elements in legacy Gmsh format"""
        num_elements = int(elements_content[0])
        elements = {}

        for i in range(1, num_elements + 1):
            parts = elements_content[i].split()
            elem_tag = int(parts[0])
            elem_type = int(parts[1])
            elem_region = int(parts[2])
            # Skip unused field
            num_nodes = int(parts[4])
            node_tags = [int(x) for x in parts[5 : 5 + num_nodes]]

            elements[elem_tag] = {
                "type": elem_type,
                "region": elem_region,
                "nodes": node_tags,
            }

        mesh_data["elements"] = elements

    def read_pre_file(self, filepath: Union[str, Path]) -> Dict:
        """
        Read a GetDP .pre file and extract DOF information.

        Args:
            filepath: Path to the .pre file

        Returns:
            Dictionary containing DOF data
        """
        filepath = Path(filepath)
        if not filepath.exists():
            raise FileNotFoundError(f"PRE file not found: {filepath}")

        dof_data = {"resolution": {}, "dof_data_blocks": []}

        with open(filepath, "r") as f:
            content = f.read()

        # Parse resolution information
        res_match = re.search(
            r"\$Resolution /\* \'(.*?)\' \*/\n(.*?)\n\$EndResolution",
            content,
            re.DOTALL,
        )
        if res_match:
            resolution_name = res_match.group(1)
            resolution_lines = res_match.group(2).strip().split("\n")
            if len(resolution_lines) >= 1:
                res_parts = resolution_lines[0].split()
                dof_data["resolution"] = {
                    "name": resolution_name,
                    "main_resolution_number": int(res_parts[0]),
                    "number_of_dofdata": int(res_parts[1]) if len(res_parts) > 1 else 0,
                }

        # Parse all DofData blocks
        dof_blocks = re.finditer(
            r"\$DofData /\* #(\d+) \*/\n(.*?)\n\$EndDofData", content, re.DOTALL
        )

        for dof_match in dof_blocks:
            dof_number = int(dof_match.group(1))
            dof_content = dof_match.group(2).strip().split("\n")

            if len(dof_content) < 5:
                continue

            # Parse header information
            resolution_number, system_number = map(int, dof_content[0].split())

            # Function spaces
            fs_line = dof_content[1].split()
            num_function_spaces = int(fs_line[0])
            function_spaces = [int(x) for x in fs_line[1 : num_function_spaces + 1]]

            # Time functions
            tf_line = dof_content[2].split()
            num_time_functions = int(tf_line[0])
            time_functions = [int(x) for x in tf_line[1 : num_time_functions + 1]]

            # Partitions
            part_line = dof_content[3].split()
            num_partitions = int(part_line[0])
            partitions = [int(x) for x in part_line[1 : num_partitions + 1]]

            # DOF counts
            dof_counts = dof_content[4].split()
            num_any_dof = int(dof_counts[0])
            num_dof = int(dof_counts[1])

            # Parse individual DOFs
            dofs = []
            for line in dof_content[5:]:
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 5:
                        dof_basis_function = int(parts[0])
                        dof_entity = int(parts[1])
                        dof_harmonic = int(parts[2])
                        dof_type = int(parts[3])

                        # Parse DOF data based on type
                        dof_data_values = parts[4:]

                        dof_entry = {
                            "basis_function_number": dof_basis_function,
                            "entity": dof_entity,
                            "harmonic": dof_harmonic,
                            "type": dof_type,
                            "type_name": self._get_dof_type_name(dof_type),
                            "data": self._parse_dof_data(dof_type, dof_data_values),
                        }
                        dofs.append(dof_entry)

            # Store the complete DofData block
            dof_block = {
                "number": dof_number,
                "resolution_number": resolution_number,
                "system_number": system_number,
                "function_spaces": function_spaces,
                "time_functions": time_functions,
                "partitions": partitions,
                "num_any_dof": num_any_dof,
                "num_dof": num_dof,
                "dofs": dofs,
            }
            dof_data["dof_data_blocks"].append(dof_block)

        self.dof_data = dof_data
        return dof_data

    def _get_dof_type_name(self, dof_type: int) -> str:
        """Get human-readable name for DOF type"""
        type_names = {
            1: "UNKNOWN",
            2: "FIXED_VALUE",
            3: "ASSOCIATED_DOF",
            5: "INITIAL_VALUE",
        }
        return type_names.get(dof_type, f"TYPE_{dof_type}")

    def _parse_dof_data(self, dof_type: int, data_values: List[str]) -> Dict:
        """Parse DOF data based on type"""
        try:
            if dof_type == 1:  # UNKNOWN
                return {
                    "equation_number": int(data_values[0])
                    if len(data_values) > 0
                    else 0,
                    "nnz": int(data_values[1]) if len(data_values) > 1 else 0,
                }
            elif dof_type == 2:  # FIXED VALUE
                return {
                    "value": float(data_values[0]) if len(data_values) > 0 else 0.0,
                    "time_function_number": int(data_values[1])
                    if len(data_values) > 1
                    else 0,
                }
            elif dof_type == 3:  # ASSOCIATED DOF
                return {
                    "associate_dof_number": int(data_values[0])
                    if len(data_values) > 0
                    else 0,
                    "value": float(data_values[1]) if len(data_values) > 1 else 0.0,
                    "time_function_number": int(data_values[2])
                    if len(data_values) > 2
                    else 0,
                }
            elif dof_type == 5:  # INITIAL VALUE
                return {
                    "equation_number": int(data_values[0])
                    if len(data_values) > 0
                    else 0,
                    "value": float(data_values[1]) if len(data_values) > 1 else 0.0,
                }
            else:
                # Unknown type, store raw data
                return {
                    "raw_data": [float(x) if "." in x else int(x) for x in data_values]
                }
        except (ValueError, IndexError):
            # Fallback to raw string data if parsing fails
            return {"raw_data": data_values}

    def read_res_file(self, filepath: Union[str, Path]) -> Dict:
        """
        Read a GetDP .res file and extract solution data.

        Args:
            filepath: Path to the .res file

        Returns:
            Dictionary containing solution data
        """
        filepath = Path(filepath)
        if not filepath.exists():
            raise FileNotFoundError(f"RES file not found: {filepath}")

        solution_data = {
            "format_info": {},
            "solutions": [],
            "mesh_nodes": {},
            "mesh_elements": {},
        }

        with open(filepath, "r") as f:
            content = f.read()

        # Check if this is a mesh-format res file or a simple solution file
        if "$MeshFormat" in content:
            # This is a mesh format file with solution data
            self._parse_res_with_mesh(content, solution_data)
        else:
            # This is a simple solution file
            self._parse_simple_res(content, solution_data)

        self.solution_data = solution_data
        return solution_data

    def _parse_res_with_mesh(self, content: str, solution_data: Dict):
        """Parse .res file that contains mesh format with solution data"""

        # Parse mesh format
        format_match = re.search(
            r"\$MeshFormat\n(.*?)\n\$EndMeshFormat", content, re.DOTALL
        )
        if format_match:
            format_line = format_match.group(1).strip()
            parts = format_line.split()
            solution_data["format_info"] = {
                "version": parts[0],
                "file_type": int(parts[1]),
                "data_size": int(parts[2]),
            }

        # Parse nodes
        nodes_match = re.search(r"\$Nodes\n(.*?)\n\$EndNodes", content, re.DOTALL)
        if nodes_match:
            nodes_content = nodes_match.group(1).strip().split("\n")
            num_nodes = int(nodes_content[0])
            nodes = {}

            for i in range(1, num_nodes + 1):
                parts = nodes_content[i].split()
                tag = int(parts[0])
                coords = [float(parts[1]), float(parts[2]), float(parts[3])]
                nodes[tag] = coords

            solution_data["mesh_nodes"] = nodes

        # Parse elements
        elements_match = re.search(
            r"\$Elements\n(.*?)\n\$EndElements", content, re.DOTALL
        )
        if elements_match:
            elements_content = elements_match.group(1).strip().split("\n")
            num_elements = int(elements_content[0])
            elements = {}

            for i in range(1, num_elements + 1):
                parts = elements_content[i].split()
                elem_tag = int(parts[0])
                elem_type = int(parts[1])
                elem_region = int(parts[2])
                num_nodes = int(parts[4])
                node_tags = [int(x) for x in parts[5 : 5 + num_nodes]]

                elements[elem_tag] = {
                    "type": elem_type,
                    "region": elem_region,
                    "nodes": node_tags,
                }

            solution_data["mesh_elements"] = elements

        # Parse node data (solution values)
        nodedata_match = re.search(
            r"\$NodeData\n(.*?)\n\$EndNodeData", content, re.DOTALL
        )
        if nodedata_match:
            nodedata_content = nodedata_match.group(1).strip().split("\n")
            self._parse_node_data(nodedata_content, solution_data)

    def _parse_simple_res(self, content: str, solution_data: Dict):
        """Parse simple .res file with just solution values"""

        # Parse format information
        format_match = re.search(
            r"\$ResFormat /\* (.*?) \*/\n(.*?)\n\$EndResFormat", content, re.DOTALL
        )
        if format_match:
            format_info = format_match.group(1)
            format_data = format_match.group(2).strip()
            solution_data["format_info"] = {
                "description": format_info,
                "version": format_data,
            }

        # Parse solution data
        solution_match = re.search(
            r"\$Solution  /\* (.*?) \*/\n(.*?)\n\$EndSolution", content, re.DOTALL
        )
        if solution_match:
            solution_info = solution_match.group(1)
            solution_content = solution_match.group(2).strip().split("\n")

            solutions = []
            for line in solution_content:
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 2:
                        value = float(parts[0])
                        # Second value is often imaginary part or additional component
                        imag_value = float(parts[1]) if len(parts) > 1 else 0.0
                        solutions.append(complex(value, imag_value))

            solution_data["solutions"] = solutions
            solution_data["solution_info"] = solution_info

    def _parse_node_data(self, nodedata_content: List[str], solution_data: Dict):
        """Parse NodeData section from mesh-format .res file"""
        # This would contain the solution values at mesh nodes
        # Implementation depends on the specific format of your NodeData sections
        pass

    def create_pyvista_mesh(
        self, res_filepath: Optional[Union[str, Path]] = None
    ) -> pv.UnstructuredGrid:
        """
        Create a PyVista mesh from the loaded GetDP data.

        Args:
            res_filepath: Optional path to .res file to load solution data

        Returns:
            PyVista UnstructuredGrid object
        """
        if not self.mesh_data or "nodes" not in self.mesh_data:
            raise ValueError("No mesh data loaded. Call read_msh_file() first.")

        # Load solution data if provided
        if res_filepath:
            self.read_res_file(res_filepath)

        # Convert nodes to numpy array
        nodes = self.mesh_data["nodes"]
        points = np.array([nodes[i] for i in sorted(nodes.keys())])

        # Convert elements to VTK format
        cells = []
        cell_types = []

        # Gmsh to VTK element type mapping
        gmsh_to_vtk = {
            1: 3,  # Line -> VTK_LINE
            2: 5,  # Triangle -> VTK_TRIANGLE
            3: 9,  # Quadrangle -> VTK_QUAD
            4: 10,  # Tetrahedron -> VTK_TETRA
            5: 12,  # Hexahedron -> VTK_HEXAHEDRON
            6: 13,  # Prism -> VTK_WEDGE
            7: 14,  # Pyramid -> VTK_PYRAMID
            15: 1,  # Point -> VTK_VERTEX
        }

        elements = self.mesh_data["elements"]
        for elem_id in sorted(elements.keys()):
            element = elements[elem_id]
            gmsh_type = element["type"]
            node_ids = element["nodes"]

            if gmsh_type in gmsh_to_vtk:
                vtk_type = gmsh_to_vtk[gmsh_type]
                # Convert to 0-based indexing
                vtk_nodes = [node_id - 1 for node_id in node_ids]
                cells.extend([len(vtk_nodes)] + vtk_nodes)
                cell_types.append(vtk_type)

        # Create PyVista mesh
        mesh = pv.UnstructuredGrid(cells, cell_types, points)

        # Add solution data if available
        if self.solution_data and "solutions" in self.solution_data:
            solutions = self.solution_data["solutions"]
            if len(solutions) == len(points):
                # Add real and imaginary parts as separate arrays
                real_parts = np.array([sol.real for sol in solutions])
                imag_parts = np.array([sol.imag for sol in solutions])

                mesh.point_data["solution_real"] = real_parts
                mesh.point_data["solution_imag"] = imag_parts
                mesh.point_data["solution_magnitude"] = np.abs(solutions)

        # Add DOF information if available
        if self.dof_data and "dof_data_blocks" in self.dof_data:
            # Process all DOF data blocks
            for dof_block in self.dof_data["dof_data_blocks"]:
                dofs = dof_block["dofs"]

                # Create arrays for DOF data
                constraint_types = np.zeros(len(points))
                constraint_values = np.zeros(len(points))
                equation_numbers = np.zeros(len(points))

                for dof in dofs:
                    entity_idx = dof["entity"] - 1  # Convert to 0-based indexing
                    if 0 <= entity_idx < len(points):
                        constraint_types[entity_idx] = dof["type"]

                        # Extract value based on DOF type
                        if dof["type"] == 2:  # FIXED_VALUE
                            constraint_values[entity_idx] = dof["data"].get(
                                "value", 0.0
                            )
                        elif dof["type"] == 1:  # UNKNOWN
                            equation_numbers[entity_idx] = dof["data"].get(
                                "equation_number", 0
                            )
                        elif dof["type"] == 5:  # INITIAL_VALUE
                            constraint_values[entity_idx] = dof["data"].get(
                                "value", 0.0
                            )
                            equation_numbers[entity_idx] = dof["data"].get(
                                "equation_number", 0
                            )

                # Add arrays to mesh (with block number suffix if multiple blocks)
                suffix = (
                    f"_block{dof_block['number']}"
                    if len(self.dof_data["dof_data_blocks"]) > 1
                    else ""
                )
                mesh.point_data[f"dof_type{suffix}"] = constraint_types
                mesh.point_data[f"dof_value{suffix}"] = constraint_values
                mesh.point_data[f"equation_number{suffix}"] = equation_numbers

        self.mesh = mesh
        return mesh

    def export_to_vtk(
        self,
        output_path: Union[str, Path],
        res_filepath: Optional[Union[str, Path]] = None,
    ):
        """
        Export the mesh and solution data to a VTK file.

        Args:
            output_path: Path where to save the VTK file
            res_filepath: Optional path to .res file to include solution data
        """
        if self.mesh is None:
            mesh = self.create_pyvista_mesh(res_filepath)
        else:
            mesh = self.mesh

        output_path = Path(output_path)
        mesh.save(str(output_path))

    def export_to_format(
        self,
        output_path: Union[str, Path],
        format_type: str = "vtk",
        res_filepath: Optional[Union[str, Path]] = None,
    ):
        """
        Export to various formats (extensible for future formats).

        Args:
            output_path: Path where to save the file
            format_type: Type of format ('vtk', 'vtu', 'ply', etc.)
            res_filepath: Optional path to .res file to include solution data
        """
        if self.mesh is None:
            mesh = self.create_pyvista_mesh(res_filepath)
        else:
            mesh = self.mesh

        output_path = Path(output_path)

        if format_type.lower() == "vtk":
            mesh.save(str(output_path))
        elif format_type.lower() == "vtu":
            mesh.save(str(output_path.with_suffix(".vtu")))
        elif format_type.lower() == "ply":
            mesh.save(str(output_path.with_suffix(".ply")))
        else:
            raise ValueError(f"Unsupported format: {format_type}")

    def get_summary(self) -> Dict:
        """
        Get a summary of the loaded data.

        Returns:
            Dictionary with summary information
        """
        summary = {}

        if self.mesh_data:
            summary["mesh"] = {
                "num_nodes": len(self.mesh_data.get("nodes", {})),
                "num_elements": len(self.mesh_data.get("elements", {})),
                "physical_regions": list(
                    self.mesh_data.get("physical_names", {}).keys()
                ),
            }

        if self.dof_data:
            total_dofs = sum(
                len(block["dofs"]) for block in self.dof_data.get("dof_data_blocks", [])
            )
            summary["dof"] = {
                "num_dof_blocks": len(self.dof_data.get("dof_data_blocks", [])),
                "total_dofs": total_dofs,
                "resolution_name": self.dof_data.get("resolution", {}).get(
                    "name", "Unknown"
                ),
                "main_resolution_number": self.dof_data.get("resolution", {}).get(
                    "main_resolution_number", 0
                ),
            }

        if self.solution_data:
            summary["solution"] = {
                "num_solutions": len(self.solution_data.get("solutions", [])),
                "has_mesh": bool(self.solution_data.get("mesh_nodes", {})),
            }

        return summary
