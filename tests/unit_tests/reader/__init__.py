"""
Shared utilities and fixtures for reader tests.

This module provides common test data, mock objects, and utility functions
used across multiple reader test files, including real file testing utilities.
"""

import numpy as np
from unittest.mock import Mock
from pathlib import Path
import tempfile
import os

# Real test file path
REAL_RAW_FILE = "tests/raw_files/Ring_Oscillator_7stage.raw"

# Known data from the real Ring Oscillator file
REAL_FILE_SIGNALS = [
    'time', 'v(bus06)', 'v(bus05)', 'v(bus09)', 'v(bus07)', 'v(bus04)', 
    'v(bus03)', 'v(vdd)', 'v(bus08)', 'v(bus10)', 'v(bus02)', 'v(bus01)', 
    'i(c1)', 'i(c2)', 'i(c3)', 'i(c4)', 'i(c5)', 'i(c6)', 'i(c7)', 
    'i(i1)', 'i(r1)', 'i(v1)', 'ix(x4:gate)', 'ix(x4:drain)', 'ix(x4:source)'
    # ... (66 total signals, showing subset for testing)
]

REAL_FILE_EXPECTED_COUNT = 66
REAL_FILE_TIME_POINTS = 2228
REAL_FILE_TIME_RANGE = (0.0, 2e-06)  # 0 to 2μs
REAL_FILE_VDD_VALUE = 2.5  # Expected VDD voltage


def get_real_file_path():
    """
    Get the absolute path to the real SPICE raw file.
    
    Returns:
        str: Absolute path to Ring_Oscillator_7stage.raw
    """
    # Get path relative to project root
    current_dir = Path(__file__).parent
    project_root = current_dir.parent.parent.parent
    return str(project_root / REAL_RAW_FILE)


def create_mock_spicelib_rawread():
    """
    Create a standardized mock spicelib.RawRead for tests.
    
    Returns:
        Mock object with get_trace_names and get_trace methods
    """
    mock_raw = Mock()
    
    # Mock signal names (original case as spicelib would return)
    mock_raw.get_trace_names.return_value = [
        "time", "V(VDD)", "V(OUT)", "I(VDD)", "V(Bus01)", "I(C1)"
    ]
    
    def get_trace_side_effect(name):
        """Mock get_trace implementation with test data."""
        trace_data = {
            "time": np.linspace(0, 1e-6, 100),
            "V(VDD)": np.ones(100) * 1.8,
            "V(OUT)": np.sin(2 * np.pi * 1e6 * np.linspace(0, 1e-6, 100)),
            "I(VDD)": np.ones(100) * 0.1,
            "V(Bus01)": np.ones(100) * 0.9,
            "I(C1)": np.ones(100) * 0.05,
        }
        
        if name in trace_data:
            return trace_data[name]
        else:
            return None  # Signal not found
    
    mock_raw.get_trace.side_effect = get_trace_side_effect
    return mock_raw


def create_mock_empty_rawread():
    """
    Create a mock RawRead with no signals for edge case testing.
    
    Returns:
        Mock object representing empty SPICE file
    """
    mock_raw = Mock()
    mock_raw.get_trace_names.return_value = []
    mock_raw.get_trace.return_value = None
    return mock_raw


def create_mock_no_time_rawread():
    """
    Create a mock RawRead without time signal for error testing.
    
    Returns:
        Mock object without time trace
    """
    mock_raw = Mock()
    mock_raw.get_trace_names.return_value = ["V(VDD)", "I(VDD)"]
    
    def get_trace_side_effect(name):
        if name == "time":
            return None  # No time data
        elif name == "V(VDD)":
            return np.ones(50) * 1.8
        elif name == "I(VDD)":
            return np.ones(50) * 0.1
        return None
    
    mock_raw.get_trace.side_effect = get_trace_side_effect
    return mock_raw


def create_temporary_invalid_file():
    """
    Create a temporary invalid file for testing file format errors.
    
    Returns:
        str: Path to temporary invalid file
    """
    temp_fd, temp_path = tempfile.mkstemp(suffix='.raw', text=True)
    try:
        with os.fdopen(temp_fd, 'w') as f:
            f.write("This is not a valid SPICE raw file\n")
            f.write("It contains invalid data\n")
    except:
        os.close(temp_fd)
        raise
    return temp_path


def assert_signal_data_integrity(data_array, expected_length=None, expected_dtype=None):
    """
    Common assertions for signal data integrity.
    
    Args:
        data_array: Numpy array to validate
        expected_length: Expected length of array (optional)
        expected_dtype: Expected data type (optional). If None, any numeric dtype is accepted.
    """
    assert isinstance(data_array, np.ndarray), "Signal data should be numpy array"
    
    if expected_dtype is not None:
        assert data_array.dtype == expected_dtype, f"Expected dtype {expected_dtype}, got {data_array.dtype}"
    else:
        # Ensure it's a numeric dtype (supports both real and complex)
        assert np.issubdtype(data_array.dtype, np.number), f"Expected numeric dtype, got {data_array.dtype}"
    
    if expected_length is not None:
        assert len(data_array) == expected_length, f"Expected length {expected_length}, got {len(data_array)}"
    
    # Check for NaN or infinite values
    assert np.all(np.isfinite(data_array)), "Signal data should not contain NaN or infinite values"


def assert_signal_list_format(signals):
    """
    Assert that signal list has correct format (lowercase, strings).
    
    Args:
        signals: List of signal names to validate
    """
    assert isinstance(signals, list), "Signals should be a list"
    
    for signal in signals:
        assert isinstance(signal, str), f"Signal name should be string, got {type(signal)}"
        assert signal == signal.lower(), f"Signal name should be lowercase: {signal}"


def assert_spice_data_info_structure(info_dict, expected_file_path=None):
    """
    Assert that info dictionary has correct structure.
    
    Args:
        info_dict: Info dictionary to validate
        expected_file_path: Expected file path (optional)
    """
    assert isinstance(info_dict, dict), "Info should be a dictionary"
    
    # Required keys
    required_keys = ["file_path", "signal_count", "signals"]
    for key in required_keys:
        assert key in info_dict, f"Info dict should contain '{key}'"
    
    # Validate types
    assert isinstance(info_dict["file_path"], str), "file_path should be string"
    assert isinstance(info_dict["signal_count"], int), "signal_count should be integer"
    assert isinstance(info_dict["signals"], list), "signals should be list"
    
    # Validate consistency
    assert info_dict["signal_count"] == len(info_dict["signals"]), \
        "signal_count should match length of signals list"
    
    if expected_file_path:
        assert info_dict["file_path"] == expected_file_path, \
            f"Expected file_path {expected_file_path}, got {info_dict['file_path']}"


def get_test_signal_variations(base_signal="V(VDD)"):
    """
    Get various case combinations for testing case insensitivity.
    
    Args:
        base_signal: Base signal name to create variations from
        
    Returns:
        List of signal name variations
    """
    if base_signal == "V(VDD)":
        return [
            "V(VDD)",      # Original case
            "v(vdd)",      # All lowercase
            "V(vdd)",      # Mixed case 1
            "v(VDD)",      # Mixed case 2
            "v(Vdd)",      # Mixed case 3
        ]
    elif base_signal == "I(C1)":
        return [
            "I(C1)",
            "i(c1)",
            "I(c1)",
            "i(C1)",
        ]
    else:
        # Generic variations
        return [
            base_signal,
            base_signal.lower(),
            base_signal.upper(),
        ]


def cleanup_temporary_file(file_path):
    """
    Safely clean up a temporary file.
    
    Args:
        file_path: Path to file to remove
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except OSError:
        pass  # Ignore cleanup errors in tests 