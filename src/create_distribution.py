import os
import uuid
from jinja2 import Environment, FileSystemLoader

# Define paths
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "..", "templates")
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "out")
TEMPLATES = ["microstrip.geo.j2", "microstrip.pro.j2"]

context = {
    "h": 8e-3,  # height of the dielectric
    "w": 7e-3,  # width of the microstrip (length in x direction)
    "t": 0.07e-2,  # thickness of the microstrip (height in y direction)
    "xBox": 1.8e-2,  # width of the air box
    "yBox": 1.2e-2,  # height of the air box
}


def main():
    # Ensure output directory exists
    os.makedirs(OUT_DIR, exist_ok=True)

    # Generate unique experiment id
    experiment_id = str(uuid.uuid4())
    experiment_dir = os.path.join(OUT_DIR, experiment_id)
    os.makedirs(experiment_dir, exist_ok=True)

    # Set up Jinja2 environment with custom delimiters
    env = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        variable_start_string="[[",
        variable_end_string="]]",
    )

    for template_name in TEMPLATES:
        template = env.get_template(template_name)
        rendered = template.render(context)
        # Remove .j2 extension for output
        output_name = template_name[:-3]
        output_path = os.path.join(experiment_dir, output_name)
        with open(output_path, "w") as f:
            f.write(rendered)
    print(f"Experiment created: {experiment_dir}")


if __name__ == "__main__":
    main()
