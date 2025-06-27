from src.experiments.microstrip import run_microstrip_experiments
from src.samplers import sample_param
import hydra
from omegaconf import DictConfig


@hydra.main(version_base=None, config_path="../config", config_name="main")
def main(cfg: DictConfig):
    exp_cfg = cfg.experiment
    n_samples = exp_cfg.n_samples
    params = exp_cfg.parameters
    output_dir = cfg.output_dir
    template_dir = cfg.get("template_dir", None)

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
