from pathlib import Path

import hydra
from omegaconf import DictConfig, OmegaConf

from src.config.experiment_config import MainConfig, dict_to_main_config
from src.experiment import experiment_registry
from src.samplers import sample_param


@hydra.main(version_base=None, config_path="../config", config_name="main")
def main(cfg: DictConfig) -> None:
    # Get the config directory path
    config_dir = Path(__file__).parent.parent / "config"

    # Convert to structured config for type safety
    structured_cfg: MainConfig = dict_to_main_config(
        OmegaConf.to_container(cfg, resolve=True), config_dir
    )

    experiments = structured_cfg.experiments
    output_dir = structured_cfg.output_dir
    template_dir = structured_cfg.template_dir

    print(f"Running {len(experiments)} experiment(s)")

    for i, exp_cfg in enumerate(experiments):
        print(
            f"\n--- Running Experiment {i + 1}/{len(experiments)}: {exp_cfg.type} ---"
        )

        n_samples = exp_cfg.n_samples
        params = exp_cfg.parameters

        print(f"Generating {n_samples} samples for {len(params)} parameters")

        # Sample values for each parameter
        sampled = {
            param: sample_param(param_cfg, n_samples)
            for param, param_cfg in params.items()
        }

        print(f"Sampled parameters: {list(sampled.keys())}")

        # Run experiment using the registry
        try:
            experiment_registry.run_experiment(
                exp_cfg=exp_cfg,
                sampled_params=sampled,
                output_dir=output_dir,
                template_dir=template_dir,
            )
            print(f"✓ Completed {exp_cfg.type} experiment")
        except Exception as e:
            print(f"✗ Error running {exp_cfg.type} experiment: {e}")
            raise


if __name__ == "__main__":
    main()
