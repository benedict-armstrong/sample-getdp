from typing import Dict, Any

from src.experiment import ParameterCfgs


def sample_context(parameters: ParameterCfgs) -> Dict[str, Any]:
    return {k: v.sample(1) for k, v in parameters.items()}
