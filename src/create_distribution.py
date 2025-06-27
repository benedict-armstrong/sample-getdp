from src.experiments.microstrip import run_microstrip_experiments
from src.samplers import sample_param
import hydra
from omegaconf import DictConfig, OmegaConf
from src.config.experiment_config import MainConfig, dict_to_main_config


@hydra.main(version_base=None, config_path="../config", config_name="main")
def main(cfg: DictConfig) -> None:
    # Convert to structured config for type safety
    structured_cfg: MainConfig = dict_to_main_config(
        OmegaConf.to_container(cfg, resolve=True)
    )
    exp_cfg = structured_cfg.experiment
    n_samples = exp_cfg.n_samples
    params = exp_cfg.parameters
    output_dir = structured_cfg.output_dir
    template_dir = structured_cfg.template_dir

    # Sample values for each parameter
    sampled = {
        param: sample_param(param_cfg, n_samples) for param, param_cfg in params.items()
    }

    run_microstrip_experiments(
        h_values=sampled["h"],
        w_values=sampled["w"],
        t_values=sampled["t"],
        xBox_values=sampled["xBox"],
        yBox_values=sampled["yBox"],
        out_dir=output_dir,
        template_dir=template_dir,
    )


if __name__ == "__main__":
    main()
