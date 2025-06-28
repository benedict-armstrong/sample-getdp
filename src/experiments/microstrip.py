import os
import uuid
import json
from jinja2 import Environment, FileSystemLoader
from dataclasses import dataclass, asdict
from typing import Sequence, Optional
from src.config.path import resolve_path

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "..", "templates")
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "out")
TEMPLATES = ["microstrip.geo.j2", "microstrip.pro.j2"]


@dataclass
class MicrostripContext:
    h: float
    w: float
    t: float
    xBox: float
    yBox: float


def run_microstrip_experiments(
    h_values: Sequence[float],
    w_values: Sequence[float],
    t_values: Sequence[float],
    xBox_values: Sequence[float],
    yBox_values: Sequence[float],
    out_dir: Optional[str] = None,
    template_dir: Optional[str] = None,
):
    """
    Runs microstrip experiments for each row of the provided parameter arrays.
    Each index corresponds to one experiment (not a Cartesian product).
    """
    resolved_out_dir = (
        resolve_path(out_dir) if out_dir is not None else resolve_path(OUT_DIR)
    )
    resolved_template_dir = (
        resolve_path(template_dir)
        if template_dir is not None
        else resolve_path(TEMPLATE_DIR)
    )
    os.makedirs(resolved_out_dir, exist_ok=True)

    env = Environment(
        loader=FileSystemLoader(resolved_template_dir),
        variable_start_string="[[",
        variable_end_string="]]",
    )

    n = len(h_values)
    assert all(
        len(arr) == n for arr in [w_values, t_values, xBox_values, yBox_values]
    ), "All parameter arrays must have the same length!"

    for i in range(n):
        ctx = MicrostripContext(
            h=h_values[i],
            w=w_values[i],
            t=t_values[i],
            xBox=xBox_values[i],
            yBox=yBox_values[i],
        )
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
            json.dump(asdict(ctx), f, indent=2)
