import os
import shutil
import uuid
from pathlib import Path
from typing import Any, Dict

import yaml
from jinja2 import Environment, FileSystemLoader


def render_template(
    context: Dict[str, Any],
    experiment_name: str,
    output_dir: Path,
    template_dir: Path,
) -> Path:
    """
    Render experiment from templates in `template_dir` and save to `output_dir`

    Returns the path to the experiment output directory
    """
    os.makedirs(output_dir, exist_ok=True)

    experiment_output_dir = output_dir / uuid.uuid4().hex[:8]
    experiment_output_dir.mkdir(parents=True, exist_ok=True)

    experiment_input_dir = template_dir / experiment_name

    # Load jinja2 environment
    env = Environment(
        loader=FileSystemLoader(experiment_input_dir),
        variable_start_string="[[",
        variable_end_string="]]",
    )

    templates = template_dir.glob("*.j2")

    # render templates
    for template_name in templates:
        template = env.get_template(template_name)
        rendered = template.render(context)
        output_name = template_name[:-3]
        output_path = os.path.join(experiment_output_dir, output_name)
        with open(output_path, "w") as f:
            f.write(rendered)

    # copy accross other files in directory
    for file in os.listdir(experiment_input_dir):
        if not file.endswith(".j2"):
            shutil.copy(experiment_input_dir / file, experiment_output_dir / file)

    # Save config
    config_path = os.path.join(experiment_output_dir, "config.yaml")
    with open(config_path, "w") as f:
        yaml.dump(context, f)

    return experiment_output_dir
