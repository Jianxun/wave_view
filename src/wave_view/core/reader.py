"""
SPICE raw file reading functionality.

This module provides the SpiceData class for reading and accessing SPICE simulation
data from .raw files using the spicelib library.
"""

from typing import List, Dict, Any, Optional
import numpy as np
from spicelib import RawRead

# Constants
MAX_SIGNALS_TO_SHOW = 5  # Maximum number of signals to show in error messages

class SpiceData:
    """
    A wrapper around spicelib.RawRead for convenient access to SPICE simulation data.
    
    This class provides a clean interface for reading SPICE .raw files and accessing
    signal data with proper type hints and error handling.
    """
    
    def __init__(self, raw_file_path: str):
        """
        Initialize SpiceData with a SPICE .raw file.
        
        Args:
            raw_file_path: Path to the SPICE .raw file
            
        Raises:
            FileNotFoundError: If the raw file doesn't exist
            Exception: If the file cannot be read by spicelib
        """
        self._raw_file_path = raw_file_path
        try:
            self._raw_data = RawRead(raw_file_path)
        except FileNotFoundError:
            raise FileNotFoundError(f"SPICE raw file not found: {raw_file_path}")
        except Exception as e:
            raise Exception(f"Failed to read SPICE raw file '{raw_file_path}': {e}")
    
    @property
    def signals(self) -> List[str]:
        """
        Get list of all available signal names in the raw file (normalized to lowercase).
        
        Returns:
            List of signal names (trace names) in lowercase
        """
        return [name.lower() for name in self._raw_data.get_trace_names()]
    
    @property
    def time(self) -> np.ndarray:
        """
        Get the time vector from the simulation.
        
        Returns:
            Time data as numpy array
            
        Raises:
            ValueError: If time data is not available
        """
        time_trace = self._raw_data.get_trace("time")
        if time_trace is None:
            raise ValueError("Time data not found in raw file")
        return np.array(time_trace, dtype=float)
    
    @property
    def info(self) -> Dict[str, Any]:
        """
        Get metadata information about the SPICE simulation.
        
        Returns:
            Dictionary containing file info and available metadata
        """
        return {
            "file_path": self._raw_file_path,
            "signal_count": len(self.signals),
            "signals": self.signals,
            # Add more metadata as available from spicelib
        }
    
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
            available_signals = ', '.join(self.signals[:MAX_SIGNALS_TO_SHOW])  # Show first 5 in lowercase
            if len(self.signals) > MAX_SIGNALS_TO_SHOW:
                available_signals += f", ... ({len(self.signals)} total)"
            raise ValueError(
                f"Signal '{name}' not found in raw file. "
                f"Available signals: {available_signals}"
            )
        
        trace = self._raw_data.get_trace(original_name)
        return np.array(trace)
    
    def get_signals(self, names: List[str]) -> Dict[str, np.ndarray]:
        """
        Get data for multiple signals (case-insensitive).
        
        Args:
            names: List of signal names - case insensitive
            
        Returns:
            Dictionary mapping normalized signal name to numpy array
            
        Raises:
            ValueError: If any signal name is not found
        """
        result = {}
        for name in names:
            normalized_name = name.lower()
            result[normalized_name] = self.get_signal(name)
        return result
    
    def has_signal(self, name: str) -> bool:
        """
        Check if a signal exists in the raw file (case-insensitive).
        
        Args:
            name: Signal name to check - case insensitive
            
        Returns:
            True if signal exists, False otherwise
        """
        return name.lower() in self.signals
    
    def __repr__(self) -> str:
        """String representation of SpiceData object."""
        return f"SpiceData('{self._raw_file_path}', {len(self.signals)} signals)" 