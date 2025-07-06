"""SPICE raw-file loading helpers for Wave View.

These high-level functions build on `WaveDataset` to give users a quick way to
obtain *(data_dict, metadata)* tuples either from a single SPICE *.raw* file or
from a batch of files (e.g. PVT / Monte-Carlo sweeps).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Tuple, Union

import numpy as np

from .core.wavedataset import WaveDataset

__all__ = [
    "load_spice_raw",
    "load_spice_raw_batch",
]

_PathLike = Union[str, Path]


def _validate_file_path(path: _PathLike) -> Path:
    """Return a *Path* after validating type, emptiness, and existence."""
    if path is None:
        raise TypeError("file path must be a string or Path object, not None")

    if isinstance(path, str) and path.strip() == "":
        raise ValueError("file path cannot be empty")

    if not isinstance(path, (str, Path)):
        raise TypeError("file path must be a string or Path object")

    file_path = Path(path).expanduser()
    if not file_path.exists():
        raise FileNotFoundError(f"SPICE raw file not found: {file_path}")

    return file_path


# ────────────────────────────────────────────────────────────────────────────
# Public API
# ────────────────────────────────────────────────────────────────────────────

def load_spice_raw(raw_file: _PathLike) -> Tuple[Dict[str, np.ndarray], Dict[str, Any]]:
    """Load one SPICE *.raw* file and return *(data_dict, metadata)*."""
    file_path = _validate_file_path(raw_file)

    wave_data = WaveDataset.from_raw(str(file_path))
    data = {sig: wave_data.get_signal(sig) for sig in wave_data.signals}
    metadata = wave_data.metadata

    return data, metadata


def load_spice_raw_batch(raw_files: List[_PathLike]) -> List[Tuple[Dict[str, np.ndarray], Dict[str, Any]]]:
    """Load many *.raw* files, preserving the order, and return a list of tuples."""
    if raw_files is None:
        raise TypeError("raw_files must be a list of file paths, not None")

    if not isinstance(raw_files, (list, tuple)):
        raise TypeError("raw_files must be a list or tuple of file paths")

    return [load_spice_raw(p) for p in raw_files] 