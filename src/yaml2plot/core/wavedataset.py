"""
WaveDataset class for SPICE simulation data with metadata support.

This module provides the WaveDataset class as a modern replacement for SpiceData,
with support for optional metadata and designed for the new v0.2.0 API.
"""

from typing import Dict, Any, Optional, List
import numpy as np
from spicelib import RawRead

# Constants
MAX_SIGNALS_TO_SHOW = 5  # Maximum number of signals to show in error messages


class WaveDataset:
    """
    A dataset container for SPICE simulation data with optional metadata.

    This class provides a clean interface for reading SPICE .raw files and accessing
    signal data with metadata support for the new v0.2.0 API.
    """

    def __init__(self, raw_data: RawRead, metadata: Optional[Dict[str, Any]] = None):
        """
        Initialize WaveDataset with raw data and optional metadata.

        Args:
            raw_data: Loaded spicelib RawRead object
            metadata: Optional metadata dictionary
        """
        self._raw_data = raw_data
        self._metadata = metadata or {}

    @property
    def signals(self) -> List[str]:
        """
        Get list of all available signal names (normalized to lowercase).

        Returns:
            List of signal names (trace names) in lowercase
        """
        return [name.lower() for name in self._raw_data.get_trace_names()]

    @property
    def metadata(self) -> Dict[str, Any]:
        """
        Get metadata dictionary associated with this dataset.

        Returns:
            Copy of metadata dictionary
        """
        return self._metadata.copy()

    def get_signal(self, name: str) -> np.ndarray:
        """
        Get data for a specific signal by name (case-insensitive).

        Args:
            name: Signal name (trace name) - case insensitive

        Returns:
            Signal data as numpy array

        Raises:
            ValueError: If signal name is not found
        """
        # Normalize input name to lowercase
        normalized_name = name.lower()

        # Find the original signal name (with original case) in the raw file
        original_signals = self._raw_data.get_trace_names()
        original_name = None

        for signal in original_signals:
            if signal.lower() == normalized_name:
                original_name = signal
                break

        if original_name is None:
            available_signals = ", ".join(
                self.signals[:MAX_SIGNALS_TO_SHOW]
            )  # Show first 5 in lowercase
            if len(self.signals) > MAX_SIGNALS_TO_SHOW:
                available_signals += f", ... ({len(self.signals)} total)"
            raise ValueError(
                f"Signal '{name}' not found in raw file. "
                f"Available signals: {available_signals}"
            )

        trace = self._raw_data.get_trace(original_name)
        return np.array(trace)

    def has_signal(self, name: str) -> bool:
        """
        Check if a signal exists in the dataset (case-insensitive).

        Args:
            name: Signal name to check - case insensitive

        Returns:
            True if signal exists, False otherwise
        """
        return name.lower() in self.signals

    @classmethod
    def from_raw(
        cls, raw_file_path: str, metadata: Optional[Dict[str, Any]] = None
    ) -> "WaveDataset":
        """
        Create WaveDataset from a SPICE .raw file.

        Args:
            raw_file_path: Path to the SPICE .raw file
            metadata: Optional metadata dictionary

        Returns:
            WaveDataset instance

        Raises:
            FileNotFoundError: If the raw file doesn't exist
            Exception: If the file cannot be read by spicelib
        """
        try:
            raw_data = RawRead(raw_file_path)
        except FileNotFoundError:
            raise FileNotFoundError(f"SPICE raw file not found: {raw_file_path}")
        except Exception as e:
            raise Exception(f"Failed to read SPICE raw file '{raw_file_path}': {e}")

        return cls(raw_data, metadata)
