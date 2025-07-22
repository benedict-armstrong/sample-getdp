from dataclasses import dataclass
from pathlib import Path
from typing import Type, TypeVar

from dacite import Config, from_dict
from omegaconf import DictConfig, OmegaConf

from src.experiment.types import ExperimentBaseCfg


@dataclass
class RootCfg:
    output_dir: Path
    experiment: ExperimentBaseCfg
    template_dir: Path = Path("templates")


TYPE_HOOKS = {
    Path: Path,
}


T = TypeVar("T")


def load_typed_config(
    cfg: DictConfig,
    data_class: Type[T],
    extra_type_hooks: dict = {},
) -> T:
    return from_dict(
        data_class,
        OmegaConf.to_container(cfg, resolve=True),
        config=Config(type_hooks={**TYPE_HOOKS, **extra_type_hooks}),
    )


def load_typed_root_config(cfg: DictConfig, configType: Type[T] = RootCfg) -> T:
    return load_typed_config(
        cfg,
        configType,
        {},
    )
