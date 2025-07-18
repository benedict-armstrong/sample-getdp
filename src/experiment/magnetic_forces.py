import os
from pathlib import Path
import uuid
import json
from jinja2 import Environment, FileSystemLoader
from dataclasses import dataclass, asdict, fields
from typing import Sequence, Optional, Dict, Any
import numpy as np
from src.config.path import resolve_path

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "..", "templates")
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "out")
TEMPLATES = ["magnets.geo.j2", "magnets.pro.j2", "magnets_common.pro.j2"]


def convert_numpy_types(obj: Any) -> Any:
    """Convert numpy types to native Python types for JSON serialization."""
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {key: convert_numpy_types(value) for key, value in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [convert_numpy_types(item) for item in obj]
    else:
        return obj


@dataclass
class MagneticForcesContext:
    num_magnets: int
    infinite_box: int  # 0 or 1
    shape: int  # 0: cylinder, 1: cube


def run_magnetic_forces_experiments(
    contexts: Sequence[MagneticForcesContext],
    out_dir: Optional[str] = None,
    template_dir: Optional[Path] = None,
):
    """
    Runs magnetic forces experiments for each MagneticForcesContext provided.
    """
    resolved_out_dir = (
        resolve_path(out_dir) if out_dir is not None else resolve_path(OUT_DIR)
    )

    # Use the provided template_dir directly, or fall back to default + subdirectory
    if template_dir is not None:
        resolved_template_dir = template_dir
    else:
        resolved_template_dir = Path(TEMPLATE_DIR) / "MagenticForces"

    os.makedirs(resolved_out_dir, exist_ok=True)

    env = Environment(
        loader=FileSystemLoader(resolved_template_dir),
        variable_start_string="[[",
        variable_end_string="]]",
    )

    for ctx in contexts:
        experiment_id = str(uuid.uuid4())
        experiment_dir = os.path.join(resolved_out_dir, experiment_id)
        os.makedirs(experiment_dir, exist_ok=True)

        # Copy the static InfiniteBox.geo file
        static_file_src = resolved_template_dir / "InfiniteBox.geo"
        static_file_dst = os.path.join(experiment_dir, "InfiniteBox.geo")
        if static_file_src.exists():
            import shutil

            shutil.copy2(static_file_src, static_file_dst)

        # Render Jinja2 templates
        for template_name in TEMPLATES:
            template = env.get_template(template_name)
            rendered = template.render(asdict(ctx))
            output_name = template_name[:-3]  # Remove .j2 extension
            output_path = os.path.join(experiment_dir, output_name)
            with open(output_path, "w") as f:
                f.write(rendered)

        # Save config
        config_path = os.path.join(experiment_dir, "config.json")
        with open(config_path, "w") as f:
            json.dump(convert_numpy_types(asdict(ctx)), f, indent=2)


def create_contexts_from_arrays(
    param_arrays: Dict[str, Sequence],
) -> Sequence[MagneticForcesContext]:
    """
    Helper function to create MagneticForcesContext objects from parameter arrays.

    Args:
        param_arrays: Dictionary mapping parameter names to sequences of values.
                     Keys should match MagneticForcesContext field names.

    Returns:
        Sequence of MagneticForcesContext objects
    """
    # Get the field names from the dataclass
    field_names = [field.name for field in fields(MagneticForcesContext)]

    # Validate that all required fields are provided
    missing_fields = set(field_names) - set(param_arrays.keys())
    if missing_fields:
        raise ValueError(f"Missing required parameter arrays: {missing_fields}")

    # Validate that all arrays have the same length
    lengths = [len(arr) for arr in param_arrays.values()]
    if not all(length == lengths[0] for length in lengths):
        raise ValueError("All parameter arrays must have the same length!")

    n = lengths[0]
    contexts = []

    for i in range(n):
        kwargs = {field_name: param_arrays[field_name][i] for field_name in field_names}
        contexts.append(MagneticForcesContext(**kwargs))

    return contexts
