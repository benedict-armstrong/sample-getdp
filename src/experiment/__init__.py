from pathlib import Path
from typing import Any, Callable, Dict, Optional, Sequence

from ..config.experiment_config import ExperimentConfig


class ExperimentRegistry:
    """Registry for experiment types and their runners."""

    def __init__(self):
        self._experiments: Dict[str, Callable] = {}
        self._context_creators: Dict[str, Callable] = {}

    def register(
        self,
        experiment_type: str,
        runner_func: Callable,
        context_creator_func: Callable,
    ):
        """Register an experiment type with its runner and context creator functions."""
        self._experiments[experiment_type] = runner_func
        self._context_creators[experiment_type] = context_creator_func

    def run_experiment(
        self,
        exp_cfg: ExperimentConfig,
        sampled_params: Dict[str, Sequence[Any]],
        output_dir: str,
        template_dir: Path,
    ):
        """Run an experiment based on its type."""
        if exp_cfg.type not in self._experiments:
            raise ValueError(f"Unknown experiment type: {exp_cfg.type}")

        # Create contexts using the registered context creator
        context_creator = self._context_creators[exp_cfg.type]
        contexts = context_creator(sampled_params)

        # Run the experiment using the registered runner
        runner = self._experiments[exp_cfg.type]
        runner(
            contexts=contexts,
            out_dir=output_dir,
            template_dir=template_dir / exp_cfg.directory,
        )

    def get_available_types(self):
        """Get list of available experiment types."""
        return list(self._experiments.keys())


# Global registry instance
experiment_registry = ExperimentRegistry()


def register_experiment(experiment_type: str):
    """Decorator to register experiment functions."""

    def decorator(func):
        # The decorated function should return (runner_func, context_creator_func)
        runner_func, context_creator_func = func()
        experiment_registry.register(experiment_type, runner_func, context_creator_func)
        return func

    return decorator


# Register available experiments
@register_experiment("microstrip")
def _register_microstrip():
    from .microstrip import create_contexts_from_arrays, run_microstrip_experiments

    return run_microstrip_experiments, create_contexts_from_arrays


# Placeholder for magnetic_forces - can be implemented later
@register_experiment("magnetic_forces")
def _register_magnetic_forces():
    def run_magnetic_forces_experiments(contexts, out_dir, template_dir):
        print(
            f"Magnetic forces experiment not yet implemented. Would run {len(contexts)} samples."
        )
        print(f"Output dir: {out_dir}, Template dir: {template_dir}")

    def create_magnetic_forces_contexts(param_arrays):
        # Placeholder - return empty list for now
        print(
            f"Creating magnetic forces contexts from params: {list(param_arrays.keys())}"
        )
        return []

    return run_magnetic_forces_experiments, create_magnetic_forces_contexts
