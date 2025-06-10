"""
Shared utilities and fixtures for config tests.

This module provides common test data, mock objects, and utility functions
used across multiple config test files, including file handling and validation utilities.
"""

import tempfile
import os
from pathlib import Path
from unittest.mock import Mock
import yaml


def create_temp_yaml_file(content, suffix='.yaml'):
    """
    Create a temporary YAML file with given content.
    
    Args:
        content: Dictionary, list, or string content for the YAML file
        suffix: File suffix (default: '.yaml')
        
    Returns:
        str: Path to temporary file
    """
    temp_fd, temp_path = tempfile.mkstemp(suffix=suffix, text=True)
    try:
        with os.fdopen(temp_fd, 'w') as f:
            if isinstance(content, (dict, list)):
                yaml.dump(content, f)
            else:
                f.write(content)
    except:
        os.close(temp_fd)
        raise
    return temp_path


def create_temp_directory_with_config(config_filename, config_content):
    """
    Create a temporary directory with a config file for testing relative paths.
    
    Args:
        config_filename: Name of config file to create
        config_content: Content for the config file
        
    Returns:
        tuple: (temp_dir_path, config_file_path)
    """
    temp_dir = tempfile.mkdtemp()
    config_path = Path(temp_dir) / config_filename
    
    with open(config_path, 'w') as f:
        if isinstance(config_content, (dict, list)):
            yaml.dump(config_content, f)
        else:
            f.write(config_content)
    
    return temp_dir, str(config_path)


def cleanup_temp_file(file_path):
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


def cleanup_temp_directory(dir_path):
    """
    Safely clean up a temporary directory and its contents.
    
    Args:
        dir_path: Path to directory to remove
    """
    try:
        import shutil
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
    except OSError:
        pass  # Ignore cleanup errors in tests


def create_mock_spice_data(signals=None):
    """
    Create a mock SpiceData object for testing validation.
    
    Args:
        signals: List of signal names (default: common test signals)
        
    Returns:
        Mock object with signals property
    """
    if signals is None:
        signals = ["time", "v(vdd)", "v(out)", "v(gnd)", "i(vdd)", "i(load)"]
    
    mock_spice_data = Mock()
    mock_spice_data.signals = signals
    return mock_spice_data


def get_basic_config_dict():
    """
    Get a basic valid configuration dictionary for testing.
    
    Returns:
        dict: Basic configuration structure
    """
    return {
        "title": "Basic Test Config",
        "X": {
            "signal_key": "raw.time",
            "label": "Time (s)"
        },
        "Y": [
            {
                "label": "Voltage",
                "signals": {
                    "VDD": "v(vdd)",
                    "OUT": "v(out)"
                }
            },
            {
                "label": "Current",
                "signals": {
                    "IDD": "i(vdd)"
                }
            }
        ]
    }





def get_config_with_log_scale():
    """
    Get a configuration with log scale settings for testing.
    
    Returns:
        dict: Configuration with log scale features
    """
    return {
        "title": "Log Scale Test",
        "X": {
            "signal_key": "raw.frequency",
            "label": "Frequency (Hz)",
            "scale": "log"
        },
        "Y": [
            {
                "label": "Magnitude (dB)",
                "scale": "log",
                "signals": {"MAG": "data.magnitude"}
            },
            {
                "label": "Phase (degrees)",
                "signals": {"PHASE": "data.phase"}
            }
        ]
    }


def get_config_with_processed_signals():
    """
    Get a configuration using processed signals for testing.
    
    Returns:
        dict: Configuration with processed signal references
    """
    return {
        "title": "Processed Signals Test",
        "X": {"signal_key": "raw.time", "label": "Time (s)"},
        "Y": [
            {
                "label": "Raw Signals",
                "signals": {"VDD": "v(vdd)", "OUT": "v(out)"}
            },
            {
                "label": "Processed Signals", 
                "signals": {
                    "POWER": "data.power",
                    "EFFICIENCY": "data.efficiency"
                }
            }
        ]
    }


def get_config_with_source_path():
    """
    Get a configuration with source file path for testing.
    
    Returns:
        dict: Configuration with source field
    """
    return {
        "source": "./test_data.raw",
        "title": "Config with Source",
        "X": {"signal_key": "raw.time", "label": "Time (s)"},
        "Y": [{"label": "Test", "signals": {"TEST": "v(test)"}}]
    }


def assert_config_structure(config_dict):
    """
    Assert that a configuration dictionary has correct structure.
    
    Args:
        config_dict: Configuration to validate
    """
    assert_single_figure_structure(config_dict)


def assert_single_figure_structure(fig_config):
    """
    Assert that a single figure configuration has correct structure.
    
    Args:
        fig_config: Single figure configuration to validate
    """
    assert isinstance(fig_config, dict), "Figure config should be a dictionary"
    assert "X" in fig_config, "Figure config should have 'X' key"
    assert "Y" in fig_config, "Figure config should have 'Y' key"
    
    # Validate X configuration
    x_config = fig_config["X"]
    assert isinstance(x_config, dict), "X config should be a dictionary"
    assert "signal_key" in x_config, "X config should have 'signal_key'"
    
    # Validate Y configuration
    y_config = fig_config["Y"]
    assert isinstance(y_config, list), "Y config should be a list"
    
    for i, y_axis in enumerate(y_config):
        assert isinstance(y_axis, dict), f"Y[{i}] should be a dictionary"
        assert "signals" in y_axis, f"Y[{i}] should have 'signals'"
        assert isinstance(y_axis["signals"], dict), f"Y[{i}]['signals'] should be a dictionary"


def assert_validation_warnings(warnings, expected_warning_count=None, contains_text=None):
    """
    Assert validation warnings meet expectations.
    
    Args:
        warnings: List of warning strings
        expected_warning_count: Expected number of warnings (optional)
        contains_text: Text that should appear in at least one warning (optional)
    """
    assert isinstance(warnings, list), "Warnings should be a list"
    
    if expected_warning_count is not None:
        assert len(warnings) == expected_warning_count, \
            f"Expected {expected_warning_count} warnings, got {len(warnings)}: {warnings}"
    
    if contains_text is not None:
        assert any(contains_text in warning for warning in warnings), \
            f"Expected warning containing '{contains_text}', got warnings: {warnings}"


def get_invalid_config_examples():
    """
    Get examples of invalid configurations for testing error handling.
    
    Returns:
        dict: Dictionary of invalid config examples with descriptions
    """
    return {
        "missing_x": {
            "config": {"Y": [{"label": "Test", "signals": {"TEST": "v(test)"}}]},
            "description": "Missing X configuration"
        },
        "missing_y": {
            "config": {"X": {"signal_key": "raw.time"}},
            "description": "Missing Y configuration"
        },
        "invalid_x_no_signal_key": {
            "config": {
                "X": {"label": "Time"},  # Missing signal_key
                "Y": [{"label": "Test", "signals": {"TEST": "v(test)"}}]
            },
            "description": "X config missing signal_key"
        },
        "invalid_y_not_list": {
            "config": {
                "X": {"signal_key": "raw.time"},
                "Y": {"not": "a list"}  # Should be a list
            },
            "description": "Y config not a list"
        },
        "invalid_y_element": {
            "config": {
                "X": {"signal_key": "raw.time"},
                "Y": [
                    {"label": "Valid", "signals": {"TEST": "v(test)"}},
                    "invalid_string"  # Should be a dict
                ]
            },
            "description": "Y contains non-dict element"
        },
        "y_missing_signals": {
            "config": {
                "X": {"signal_key": "raw.time"},
                "Y": [{"label": "Missing Signals"}]  # No 'signals' key
            },
            "description": "Y element missing signals"
        },
        "y_invalid_signals_type": {
            "config": {
                "X": {"signal_key": "raw.time"},
                "Y": [{"label": "Test", "signals": "should_be_dict"}]
            },
            "description": "Y element signals not a dict"
        }
    }


def get_yaml_test_strings():
    """
    Get various YAML string examples for testing content detection.
    
    Returns:
        dict: YAML examples categorized by type
    """
    return {
        "simple_yaml": "title: Test\nX:\n  signal_key: raw.time",
        "multiline_yaml": """
title: "Multi-line Test"
X:
  signal_key: "raw.time"
  label: "Time (s)"
Y:
  - label: "Voltage"
    signals:
      VDD: "v(vdd)"
""",
        "list_yaml": """
- title: "Figure 1"
  X:
    signal_key: "raw.time"
  Y: []
- title: "Figure 2"
  X:
    signal_key: "raw.freq"
  Y: []
""",
        "file_paths": [
            "config.yaml",
            "my_config.yml", 
            "path/to/config.yaml",
            "./relative/config.yml",
            "/absolute/path/config.yaml"
        ],
        "not_file_paths": [
            "title: Test Config",
            "X: {signal_key: raw.time}",
            "- item1\n- item2",
            "key: value\nother: content"
        ]
    } 