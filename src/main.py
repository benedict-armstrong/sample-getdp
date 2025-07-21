from typing import List

import hydra
import tqdm
from omegaconf import DictConfig

from src.config import RootCfg, load_typed_root_config
from src.experiment import Experiment


@hydra.main(
    version_base=None,
    config_path="../config",
    config_name="main",
)
def main(cfg_dict: DictConfig) -> None:
    cfg: RootCfg = load_typed_root_config(cfg_dict)

    # Step one create the experiments by samling from the parameters
    experiments: List[Experiment] = []
    for i in tqdm.trange(cfg.experiment.n_samples):
        ex = Experiment.sample(
            cfg.experiment.parameters, cfg.output_dir, cfg.template_dir
        )
        experiments.append(ex)

    # Step two run the experiment
    for experiment in tqdm.tqdm(experiments):
        experiment.run()

    # Step three run the post processing
    for experiment in tqdm.tqdm(experiments):
        experiment.post_process()


if __name__ == "__main__":
    main()
