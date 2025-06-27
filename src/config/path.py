from typing import Optional
import hydra
import os
from pathlib import Path


def resolve_path(path: Optional[str] | Path) -> Optional[Path]:
    """
    Resolve a path relative to the original working directory if not absolute.
    If path is None, returns None.
    """
    if path is None:
        return None
    if os.path.isabs(path):
        return Path(path)

    return Path(os.path.join(hydra.utils.get_original_cwd(), path))
