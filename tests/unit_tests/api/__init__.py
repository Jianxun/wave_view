"""
Shared utilities and fixtures for API tests.

This module provides common test data, mock objects, and utility functions
used across multiple API test files, including mock SPICE data and test configurations.
"""

import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import yaml
import numpy as np
import plotly.graph_objects as go


def create_temp_raw_file(filename="test.raw"):
    """
    Create a temporary raw file for testing.
    
    Args:
        filename: Name for the temporary file
        
    Returns:
        str: Path to temporary file
    """
    temp_fd, temp_path = tempfile.mkstemp(suffix='.raw', text=False)
    os.close(temp_fd)
    return temp_path


def create_temp_yaml_config(config_dict, suffix='.yaml'):
    """
    Create a temporary YAML configuration file.
    
    Args:
        config_dict: Configuration dictionary to write
        suffix: File suffix (default: '.yaml')
        
    Returns:
        str: Path to temporary file
    """
    temp_fd, temp_path = tempfile.mkstemp(suffix=suffix, text=True)
    try:
        with os.fdopen(temp_fd, 'w') as f:
            yaml.dump(config_dict, f)
    except:
        os.close(temp_fd)
        raise
    return temp_path


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


def create_mock_spice_data(signals=None, time_data=None):
    """
    Create a mock SpiceData object for testing.
    
    Args:
        signals: List of signal names (default: common test signals)
        time_data: Optional time array data
        
    Returns:
        Mock SpiceData object
    """
    if signals is None:
        signals = ["time", "v(vdd)", "v(out)", "v(gnd)", "i(vdd)", "i(load)"]
    
    if time_data is None:
        time_data = np.linspace(0, 1e-6, 1000)
    
    mock_spice_data = Mock()
    mock_spice_data.signals = signals
    mock_spice_data.info = {
        "title": "Test Simulation",
        "date": "Test Date",
        "plotname": "Test Plot",
        "flags": "real",
        "no_vars": len(signals),
        "no_points": len(time_data),
        "variables": []
    }
    
    # Mock get_signal method
    def mock_get_signal(signal_name):
        # Return different test data based on signal name
        if signal_name.lower() == "time":
            return time_data
        elif signal_name.lower().startswith("v("):
            # Voltage signal - sine wave
            return 1.8 + 0.1 * np.sin(2 * np.pi * 1e6 * time_data)
        elif signal_name.lower().startswith("i("):
            # Current signal - cosine wave
            return 1e-3 * np.cos(2 * np.pi * 1e6 * time_data)
        else:
            # Generic signal
            return np.random.random(len(time_data))
    
    mock_spice_data.get_signal = Mock(side_effect=mock_get_signal)
    return mock_spice_data


def create_mock_spice_plotter(mock_spice_data=None, return_figure=None):
    """
    Create a mock SpicePlotter object for testing.
    
    Args:
        mock_spice_data: Optional SpiceData mock to use
        return_figure: Optional figure to return from create_figure()
        
    Returns:
        Mock SpicePlotter object
    """
    if mock_spice_data is None:
        mock_spice_data = create_mock_spice_data()
    
    if return_figure is None:
        return_figure = go.Figure()
        return_figure.add_trace(go.Scatter(x=[1, 2, 3], y=[1, 2, 3], name="Test"))
    
    mock_plotter = Mock()
    mock_plotter.data = mock_spice_data
    mock_plotter._processed_signals = {}
    mock_plotter.load_config = Mock()
    mock_plotter.create_figure = Mock(return_value=return_figure)
    
    return mock_plotter


def get_basic_test_config():
    """
    Get a basic configuration dictionary for testing.
    
    Returns:
        dict: Basic test configuration
    """
    return {
        "title": "API Test Configuration",
        "X": {
            "signal_key": "raw.time",
            "label": "Time (s)"
        },
        "Y": [
            {
                "label": "Voltage (V)",
                "signals": {
                    "VDD": "v(vdd)",
                    "OUT": "v(out)"
                }
            },
            {
                "label": "Current (A)",
                "signals": {
                    "IDD": "i(vdd)"
                }
            }
        ]
    }


def get_multi_figure_test_config():
    """
    Get a multi-figure configuration list for testing rejection.
    
    This configuration should be rejected by the current system
    since multi-figure support has been removed.
    
    Returns:
        list: Multi-figure test configuration (for rejection testing)
    """
    return [
        {
            "title": "Voltages",
            "X": {"signal_key": "raw.time", "label": "Time (s)"},
            "Y": [{"label": "Voltage", "signals": {"VDD": "v(vdd)"}}]
        },
        {
            "title": "Currents",
            "X": {"signal_key": "raw.time", "label": "Time (s)"},
            "Y": [{"label": "Current", "signals": {"IDD": "i(vdd)"}}]
        }
    ]


def get_processed_data_config():
    """
    Get a configuration that uses processed data.
    
    Returns:
        dict: Configuration with processed data references
    """
    return {
        "title": "Processed Data Test",
        "X": {
            "signal_key": "raw.time",
            "label": "Time (s)"
        },
        "Y": [
            {
                "label": "Magnitude (dB)",
                "signals": {
                    "MAG": "data.magnitude"
                }
            },
            {
                "label": "Phase (deg)",
                "signals": {
                    "PHASE": "data.phase"
                }
            }
        ]
    }


def get_log_scale_config():
    """
    Get a configuration with log scale settings.
    
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
            }
        ]
    }


def get_test_processed_data():
    """
    Get sample processed data for testing.
    
    Returns:
        dict: Sample processed data arrays
    """
    time_data = np.linspace(0, 1e-6, 1000)
    return {
        "magnitude": 20 * np.log10(np.abs(np.sin(2 * np.pi * 1e6 * time_data) + 1j * np.cos(2 * np.pi * 1e6 * time_data))),
        "phase": np.angle(np.sin(2 * np.pi * 1e6 * time_data) + 1j * np.cos(2 * np.pi * 1e6 * time_data)) * 180 / np.pi,
        "power": np.abs(np.sin(2 * np.pi * 1e6 * time_data)) * 0.001
    }


def assert_figure_properties(figure, expected_traces=None, expected_title=None):
    """
    Assert properties of a Plotly figure.
    
    Args:
        figure: Plotly Figure object to check
        expected_traces: Expected number of traces (optional)
        expected_title: Expected figure title (optional)
    """
    assert isinstance(figure, go.Figure), "Expected Plotly Figure object"
    
    if expected_traces is not None:
        assert len(figure.data) == expected_traces, f"Expected {expected_traces} traces, got {len(figure.data)}"
    
    if expected_title is not None:
        assert figure.layout.title.text == expected_title, f"Expected title '{expected_title}', got '{figure.layout.title.text}'"


def get_yaml_config_string():
    """
    Get a YAML configuration as a string for testing.
    
    Returns:
        str: YAML configuration string
    """
    return '''
title: "YAML String Test"
X:
  signal_key: "raw.time"
  label: "Time (s)"
Y:
  - label: "Voltage (V)"
    signals:
      VDD: "v(vdd)"
      OUT: "v(out)"
'''


def get_template_config_structure():
    """
    Get the expected structure for a template configuration.
    
    Returns:
        dict: Expected template structure
    """
    return {
        "title": "SPICE Waveform Plot",
        "source": "./simulation.raw",
        "X": {
            "signal_key": "raw.time",
            "label": "Time (s)"
        },
        "Y": [],
        "plot_height": 600,
        "show_rangeslider": True,
        "show_zoom_buttons": True,
        "default_dragmode": "zoom"
    }


class MockEnvironment:
    """Context manager for mocking environment detection."""
    
    def __init__(self, is_jupyter=False, is_colab=False):
        self.is_jupyter = is_jupyter
        self.is_colab = is_colab
        self.patches = []
    
    def __enter__(self):
        if self.is_jupyter:
            # Mock IPython environment
            mock_ipython = Mock()
            mock_ipython.kernel = True
            mock_get_ipython = Mock(return_value=mock_ipython)
            self.patches.append(patch('wave_view.api.get_ipython', mock_get_ipython))
        else:
            # Mock no IPython
            self.patches.append(patch('wave_view.api.get_ipython', side_effect=ImportError))
        
        if self.is_colab:
            # Mock Google Colab
            self.patches.append(patch('wave_view.api.google.colab', create=True))
        else:
            # Mock no Colab
            self.patches.append(patch('wave_view.api.google.colab', side_effect=ImportError, create=True))
        
        # Start all patches
        for p in self.patches:
            p.start()
        
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Stop all patches
        for p in self.patches:
            p.stop() 