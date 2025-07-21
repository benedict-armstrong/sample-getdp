from typing import Any, Dict

from src.experiment.types import ParameterCfgs


def sample_context(parameters: ParameterCfgs) -> Dict[str, Any]:
    return {k: v.sample(1) for k, v in parameters.items()}
