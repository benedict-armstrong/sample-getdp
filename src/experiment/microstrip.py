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
TEMPLATES = ["microstrip.geo.j2", "microstrip.pro.j2"]


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
class MicrostripContext:
    h: float
    w: float
    t: float
    xBox: float
    yBox: float
    initial_voltage: float


def run_microstrip_experiments(
    contexts: Sequence[MicrostripContext],
    out_dir: Optional[str] = None,
    template_dir: Optional[Path] = None,
):
    """
    Runs microstrip experiments for each MicrostripContext provided.
    """
    resolved_out_dir = (
        resolve_path(out_dir) if out_dir is not None else resolve_path(OUT_DIR)
    )
    resolved_template_dir = (
        template_dir if template_dir is not None else Path(TEMPLATE_DIR)
    )
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
        # Render templates
        for template_name in TEMPLATES:
            template = env.get_template(template_name)
            rendered = template.render(asdict(ctx))
            output_name = template_name[:-3]
            output_path = os.path.join(experiment_dir, output_name)
            with open(output_path, "w") as f:
                f.write(rendered)
        # Save config
        config_path = os.path.join(experiment_dir, "config.json")
        with open(config_path, "w") as f:
            json.dump(convert_numpy_types(asdict(ctx)), f, indent=2)


def create_contexts_from_arrays(
    param_arrays: Dict[str, Sequence[float]],
) -> Sequence[MicrostripContext]:
    """
    Helper function to create MicrostripContext objects from parameter arrays.

    Args:
        param_arrays: Dictionary mapping parameter names to sequences of values.
                     Keys should match MicrostripContext field names.

    Returns:
        Sequence of MicrostripContext objects
    """
    # Get the field names from the dataclass
    field_names = [field.name for field in fields(MicrostripContext)]

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
        contexts.append(MicrostripContext(**kwargs))

    return contexts
