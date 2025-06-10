"""
Shared utilities and fixtures for plotter tests.

This module provides common test data, mock objects, and utility functions
used across multiple plotter test files.
"""

import numpy as np
from unittest.mock import Mock
from wave_view.core.config import PlotConfig


def create_mock_spice_data():
    """
    Create a standardized mock SpiceData for tests.
    
    Returns:
        Mock object with signals and get_signal method
    """
    mock_data = Mock()
    mock_data.signals = ["time", "v(vdd)", "v(out)", "i(vdd)", "frequency"]
    
    def get_signal_side_effect(name):
        """Mock get_signal implementation with test data."""
        signal_data = {
            "time": np.linspace(0, 1e-6, 100),
            "v(vdd)": np.ones(100) * 1.8,
            "v(out)": np.sin(2 * np.pi * 1e6 * np.linspace(0, 1e-6, 100)),
            "i(vdd)": np.ones(100) * 0.1,
            "frequency": np.logspace(3, 9, 100)  # 1kHz to 1GHz
        }
        
        normalized_name = name.lower()
        if normalized_name in signal_data:
            return signal_data[normalized_name]
        else:
            raise ValueError(f"Signal '{name}' not found in mock data")
    
    mock_data.get_signal.side_effect = get_signal_side_effect
    return mock_data


def create_basic_config():
    """
    Create a basic single-figure test configuration.
    
    Returns:
        PlotConfig object with simple time-domain plot
    """
    return PlotConfig({
        "title": "Basic Test Plot",
        "X": {"signal_key": "raw.time", "label": "Time (s)"},
        "Y": [{"label": "Voltage", "signals": {"VDD": "v(vdd)"}}]
    })


def create_multi_axis_config():
    """
    Create a multi-Y-axis test configuration.
    
    Returns:
        PlotConfig object with multiple Y-axes
    """
    return PlotConfig({
        "title": "Multi-Axis Test Plot",
        "X": {"signal_key": "raw.time", "label": "Time (s)"},
        "Y": [
            {"label": "Voltage", "signals": {"VDD": "v(vdd)", "OUT": "v(out)"}},
            {"label": "Current", "signals": {"IDD": "i(vdd)"}}
        ]
    })


def create_log_scale_config():
    """
    Create a configuration with log scales.
    
    Returns:
        PlotConfig object with log-scaled axes
    """
    return PlotConfig({
        "title": "Log Scale Test",
        "X": {"signal_key": "raw.frequency", "label": "Frequency (Hz)", "scale": "log"},
        "Y": [{"label": "Magnitude", "scale": "log", "signals": {"OUT": "v(out)"}}]
    })


def create_mixed_scale_config():
    """
    Create a configuration with mixed linear/log Y-axes.
    
    Returns:
        PlotConfig object with mixed scale types
    """
    return PlotConfig({
        "title": "Mixed Scale Test",
        "X": {"signal_key": "raw.time", "label": "Time (s)"},
        "Y": [
            {"label": "Linear Voltage", "signals": {"VDD": "v(vdd)"}},
            {"label": "Log Current", "scale": "log", "signals": {"IDD": "i(vdd)"}}
        ]
    })


def create_processed_signals_config():
    """
    Create a configuration that uses processed signals.
    
    Returns:
        PlotConfig object referencing processed signals with "data." prefix
    """
    return PlotConfig({
        "title": "Processed Signals Test",
        "X": {"signal_key": "raw.time", "label": "Time (s)"},
        "Y": [
            {"label": "Raw Voltage", "signals": {"VDD": "v(vdd)"}},
            {"label": "Processed Power", "signals": {"POWER": "data.power"}}
        ]
    })





def assert_figure_structure(fig, expected_traces=1, title="Basic Test Plot"):
    """
    Common assertions for Plotly figure structure.
    
    Args:
        fig: Plotly Figure object
        expected_traces: Expected number of traces
        title: Expected plot title
    """
    # Basic figure structure
    assert hasattr(fig, 'data'), "Figure should have data attribute"
    assert hasattr(fig, 'layout'), "Figure should have layout attribute"
    
    # Check number of traces
    assert len(fig.data) == expected_traces, f"Expected {expected_traces} traces, got {len(fig.data)}"
    
    # Check title
    assert fig.layout.title.text == title, f"Expected title '{title}', got '{fig.layout.title.text}'"
    
    # Check axes exist
    assert hasattr(fig.layout, 'xaxis'), "Figure should have xaxis"
    assert hasattr(fig.layout, 'yaxis'), "Figure should have yaxis"


def assert_trace_data_integrity(trace, expected_length=100):
    """
    Assert that trace data has correct structure and length.
    
    Args:
        trace: Plotly trace object
        expected_length: Expected length of data arrays
    """
    assert hasattr(trace, 'x'), "Trace should have x data"
    assert hasattr(trace, 'y'), "Trace should have y data"
    assert len(trace.x) == expected_length, f"Expected x data length {expected_length}, got {len(trace.x)}"
    assert len(trace.y) == expected_length, f"Expected y data length {expected_length}, got {len(trace.y)}"
    assert hasattr(trace, 'name'), "Trace should have name"


def assert_log_scale_applied(axis_layout, should_be_log=True):
    """
    Assert that log scale is correctly applied to axis layout.
    
    Args:
        axis_layout: Plotly axis layout object
        should_be_log: Whether axis should have log scale
    """
    if should_be_log:
        assert getattr(axis_layout, 'type', None) == 'log', "Axis should have log scale type"
    else:
        assert getattr(axis_layout, 'type', None) != 'log', "Axis should not have log scale type"


def assert_multi_yaxis_domains(fig, num_y_axes):
    """
    Assert that multi-Y-axis domains are correctly calculated.
    
    Args:
        fig: Plotly Figure object
        num_y_axes: Expected number of Y-axes
    """
    if num_y_axes == 1:
        # Single Y-axis should use full domain
        assert fig.layout.yaxis.domain == [0, 1], "Single Y-axis should use full domain"
    else:
        # Multi-Y-axes should have non-overlapping domains
        gap = 0.05
        total_gap_space = gap * (num_y_axes - 1)
        effective_height = 1.0 - total_gap_space
        single_height = effective_height / num_y_axes
        
        for i in range(num_y_axes):
            axis_name = 'yaxis' if i == 0 else f'yaxis{i + 1}'
            axis = getattr(fig.layout, axis_name)
            
            expected_bottom = i * (single_height + gap)
            expected_top = expected_bottom + single_height
            
            assert abs(axis.domain[0] - expected_bottom) < 0.01, f"Y-axis {i+1} domain bottom incorrect"
            assert abs(axis.domain[1] - expected_top) < 0.01, f"Y-axis {i+1} domain top incorrect" 