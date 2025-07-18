from typing import List
import hydra
import tqdm

from omegaconf import DictConfig

from src.config import RootCfg, load_typed_root_config
from src.experiment import Experiment, get_experiment


@hydra.main(
    version_base=None,
    config_path="../config",
    config_name="main",
)
def main(cfg_dict: DictConfig) -> None:
    cfg: RootCfg = load_typed_root_config(cfg_dict)

    # Step one create the experiments by samling from the parameters
    experiment = get_experiment(cfg.experiment)

    experiments: List[Experiment] = []
    for i in tqdm.trange(cfg.experiment.n_samples):
        experiment.sample(cfg.output_dir)

    # Step two run the experiment
    for experiment in tqdm.tqdm(experiments):
        experiment.run()


if __name__ == "__main__":
    main()
