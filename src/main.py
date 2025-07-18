import hydra
from omegaconf import DictConfig

from src.config import RootCfg, load_typed_root_config


@hydra.main(
    version_base=None,
    config_path="../config",
    config_name="main",
)
def main(cfg_dict: DictConfig) -> None:
    cfg: RootCfg = load_typed_root_config(cfg_dict)

    print(cfg)


if __name__ == "__main__":
    main()
