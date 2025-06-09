"""
Unit tests for SpicePlotter log scale functionality.

This module tests the log scale support for both X and Y axes,
including configuration application and figure layout verification.
"""

import unittest
from unittest.mock import Mock, patch
import numpy as np

from wave_view.core.plotter import SpicePlotter
from . import (create_mock_spice_data, create_log_scale_config, 
               create_mixed_scale_config, assert_log_scale_applied,
               assert_figure_structure)


class TestXAxisLogScale(unittest.TestCase):
    """Test X-axis log scale functionality."""
    
    @patch('wave_view.core.plotter.SpiceData')
    def test_x_axis_log_scale_applied(self, mock_spice_data_class):
        """Test that X-axis log scale is correctly applied to figure."""
        mock_spice_data_class.return_value = create_mock_spice_data()
        
        plotter = SpicePlotter("test.raw")
        plotter.load_config(create_log_scale_config())
        
        fig = plotter.create_figure()
        
        # Check basic figure structure
        assert_figure_structure(fig, expected_traces=1, title="Log Scale Test")
        
        # Check X-axis has log scale
        assert_log_scale_applied(fig.layout.xaxis, should_be_log=True)
        self.assertEqual(fig.layout.xaxis.type, "log")
    
    @patch('wave_view.core.plotter.SpiceData')
    def test_x_axis_linear_scale_default(self, mock_spice_data_class):
        """Test that X-axis defaults to linear scale when not specified."""
        mock_spice_data_class.return_value = create_mock_spice_data()
        
        # Config without scale specified (should default to linear)
        linear_config = {
            "title": "Linear X Scale Test",
            "X": {"signal_key": "raw.time", "label": "Time (s)"},  # No scale specified
            "Y": [{"label": "Voltage", "signals": {"VDD": "v(vdd)"}}]
        }
        
        plotter = SpicePlotter("test.raw")
        plotter.load_config(linear_config)
        
        fig = plotter.create_figure()
        
        # Check X-axis does not have log scale
        assert_log_scale_applied(fig.layout.xaxis, should_be_log=False)
        self.assertNotEqual(getattr(fig.layout.xaxis, 'type', None), "log")
    
    @patch('wave_view.core.plotter.SpiceData')
    def test_x_axis_explicit_linear_scale(self, mock_spice_data_class):
        """Test X-axis with explicitly set linear scale."""
        mock_spice_data_class.return_value = create_mock_spice_data()
        
        linear_config = {
            "title": "Explicit Linear X",
            "X": {"signal_key": "raw.time", "label": "Time (s)", "scale": "linear"},
            "Y": [{"label": "Voltage", "signals": {"VDD": "v(vdd)"}}]
        }
        
        plotter = SpicePlotter("test.raw")
        plotter.load_config(linear_config)
        
        fig = plotter.create_figure()
        
        # Check X-axis does not have log scale
        assert_log_scale_applied(fig.layout.xaxis, should_be_log=False)


class TestYAxisLogScale(unittest.TestCase):
    """Test Y-axis log scale functionality."""
    
    @patch('wave_view.core.plotter.SpiceData')
    def test_single_y_axis_log_scale(self, mock_spice_data_class):
        """Test single Y-axis with log scale."""
        mock_spice_data_class.return_value = create_mock_spice_data()
        
        plotter = SpicePlotter("test.raw")
        plotter.load_config(create_log_scale_config())
        
        fig = plotter.create_figure()
        
        # Check Y-axis has log scale
        assert_log_scale_applied(fig.layout.yaxis, should_be_log=True)
        self.assertEqual(fig.layout.yaxis.type, "log")
    
    @patch('wave_view.core.plotter.SpiceData')
    def test_mixed_y_axis_scales(self, mock_spice_data_class):
        """Test multiple Y-axes with different scales."""
        mock_spice_data_class.return_value = create_mock_spice_data()
        
        plotter = SpicePlotter("test.raw")
        plotter.load_config(create_mixed_scale_config())
        
        fig = plotter.create_figure()
        
        # Due to Y-axis reversal in plotter: 
        # - "Log Current" (second in config) becomes yaxis (first plotly axis)
        # - "Linear Voltage" (first in config) becomes yaxis2 (second plotly axis)
        
        # Check yaxis (Log Current - should have log scale)
        assert_log_scale_applied(fig.layout.yaxis, should_be_log=True)
        self.assertEqual(fig.layout.yaxis.type, "log")
        
        # Check yaxis2 (Linear Voltage - should not have log scale)
        assert_log_scale_applied(fig.layout.yaxis2, should_be_log=False)
    
    @patch('wave_view.core.plotter.SpiceData')
    def test_multiple_y_axes_all_log(self, mock_spice_data_class):
        """Test multiple Y-axes all with log scale."""
        mock_spice_data_class.return_value = create_mock_spice_data()
        
        all_log_config = {
            "title": "All Log Y-Axes",
            "X": {"signal_key": "raw.time", "label": "Time (s)"},
            "Y": [
                {
                    "label": "Log Voltage",
                    "scale": "log",
                    "signals": {"VDD": "v(vdd)"}
                },
                {
                    "label": "Log Current", 
                    "scale": "log",
                    "signals": {"IDD": "i(vdd)"}
                },
                {
                    "label": "Log Output",
                    "scale": "log", 
                    "signals": {"OUT": "v(out)"}
                }
            ]
        }
        
        plotter = SpicePlotter("test.raw")
        plotter.load_config(all_log_config)
        
        fig = plotter.create_figure()
        
        # Check all Y-axes have log scale
        assert_log_scale_applied(fig.layout.yaxis, should_be_log=True)
        assert_log_scale_applied(fig.layout.yaxis2, should_be_log=True)
        assert_log_scale_applied(fig.layout.yaxis3, should_be_log=True)
        
        self.assertEqual(fig.layout.yaxis.type, "log")
        self.assertEqual(fig.layout.yaxis2.type, "log")
        self.assertEqual(fig.layout.yaxis3.type, "log")


class TestBothAxesLogScale(unittest.TestCase):
    """Test configurations with both X and Y axes using log scale."""
    
    @patch('wave_view.core.plotter.SpiceData')
    def test_both_axes_log_scale(self, mock_spice_data_class):
        """Test configuration with both X and Y axes log scale."""
        mock_spice_data_class.return_value = create_mock_spice_data()
        
        both_log_config = {
            "title": "Both Axes Log Scale",
            "X": {
                "signal_key": "raw.frequency",
                "label": "Frequency (Hz)",
                "scale": "log"
            },
            "Y": [
                {
                    "label": "Magnitude (dB)",
                    "scale": "log",
                    "signals": {"MAG": "v(out)"}
                }
            ]
        }
        
        plotter = SpicePlotter("test.raw")
        plotter.load_config(both_log_config)
        
        fig = plotter.create_figure()
        
        # Check both axes have log scale
        assert_log_scale_applied(fig.layout.xaxis, should_be_log=True)
        assert_log_scale_applied(fig.layout.yaxis, should_be_log=True)
        
        self.assertEqual(fig.layout.xaxis.type, "log")
        self.assertEqual(fig.layout.yaxis.type, "log")
    
    @patch('wave_view.core.plotter.SpiceData')
    def test_bode_plot_configuration(self, mock_spice_data_class):
        """Test typical Bode plot configuration (log freq, log magnitude)."""
        mock_spice_data_class.return_value = create_mock_spice_data()
        
        bode_config = {
            "title": "Bode Plot",
            "X": {
                "signal_key": "raw.frequency",
                "label": "Frequency (Hz)",
                "scale": "log"
            },
            "Y": [
                {
                    "label": "Magnitude (dB)",
                    "scale": "log",
                    "signals": {"MAGNITUDE": "v(out)"}
                },
                {
                    "label": "Phase (degrees)",
                    "scale": "linear",  # Phase typically linear
                    "signals": {"PHASE": "v(vdd)"}
                }
            ]
        }
        
        plotter = SpicePlotter("test.raw")
        plotter.load_config(bode_config)
        
        fig = plotter.create_figure()
        
        # Check X-axis log scale
        assert_log_scale_applied(fig.layout.xaxis, should_be_log=True)
        
        # Due to Y-axis reversal in plotter:
        # - "Phase (degrees)" (second in config) becomes yaxis (first plotly axis)
        # - "Magnitude (dB)" (first in config) becomes yaxis2 (second plotly axis)
        
        # Check yaxis (Phase - should have linear scale)
        assert_log_scale_applied(fig.layout.yaxis, should_be_log=False)
        
        # Check yaxis2 (Magnitude - should have log scale) 
        assert_log_scale_applied(fig.layout.yaxis2, should_be_log=True)
        self.assertEqual(fig.layout.yaxis2.type, "log")


class TestLogScaleEdgeCases(unittest.TestCase):
    """Test edge cases and error conditions for log scale."""
    
    @patch('wave_view.core.plotter.SpiceData')
    def test_invalid_scale_value_ignored(self, mock_spice_data_class):
        """Test that invalid scale values are ignored (default to linear)."""
        mock_spice_data_class.return_value = create_mock_spice_data()
        
        invalid_scale_config = {
            "title": "Invalid Scale Test",
            "X": {
                "signal_key": "raw.time",
                "label": "Time (s)",
                "scale": "invalid_scale"  # Invalid scale value
            },
            "Y": [
                {
                    "label": "Voltage",
                    "scale": "also_invalid",  # Invalid scale value
                    "signals": {"VDD": "v(vdd)"}
                }
            ]
        }
        
        plotter = SpicePlotter("test.raw")
        plotter.load_config(invalid_scale_config)
        
        fig = plotter.create_figure()
        
        # Both axes should default to linear (no log scale applied)
        assert_log_scale_applied(fig.layout.xaxis, should_be_log=False)
        assert_log_scale_applied(fig.layout.yaxis, should_be_log=False)
    
    @patch('wave_view.core.plotter.SpiceData')
    def test_log_scale_with_processed_signals(self, mock_spice_data_class):
        """Test log scale with processed signals."""
        mock_spice_data_class.return_value = create_mock_spice_data()
        
        processed_log_config = {
            "title": "Log Scale with Processed Signals",
            "X": {"signal_key": "raw.frequency", "scale": "log"},
            "Y": [
                {
                    "label": "Power (W)",
                    "scale": "log",
                    "signals": {"POWER": "data.power"}
                }
            ]
        }
        
        plotter = SpicePlotter("test.raw")
        plotter.load_config(processed_log_config)
        plotter.add_processed_signal("power", lambda d: d["v(vdd)"] * d["i(vdd)"])
        
        fig = plotter.create_figure()
        
        # Check log scales are applied
        assert_log_scale_applied(fig.layout.xaxis, should_be_log=True)
        assert_log_scale_applied(fig.layout.yaxis, should_be_log=True)
        
        # Check that figure was created successfully with processed data
        self.assertGreater(len(fig.data), 0)
    
    @patch('wave_view.core.plotter.SpiceData')
    def test_log_scale_case_insensitive(self, mock_spice_data_class):
        """Test that log scale specification is case-insensitive."""
        mock_spice_data_class.return_value = create_mock_spice_data()
        
        case_config = {
            "title": "Case Insensitive Scale",
            "X": {"signal_key": "raw.time", "scale": "LOG"},  # Uppercase
            "Y": [
                {
                    "label": "Voltage",
                    "scale": "Log",  # Mixed case
                    "signals": {"VDD": "v(vdd)"}
                }
            ]
        }
        
        plotter = SpicePlotter("test.raw")
        plotter.load_config(case_config)
        
        fig = plotter.create_figure()
        
        # Note: Current implementation is case-sensitive, expecting "log"
        # This test documents current behavior - may need update if case-insensitive support added
        assert_log_scale_applied(fig.layout.xaxis, should_be_log=False)  # "LOG" != "log"
        assert_log_scale_applied(fig.layout.yaxis, should_be_log=False)   # "Log" != "log"


class TestLogScaleDataIntegrity(unittest.TestCase):
    """Test that log scale doesn't affect data integrity."""
    
    @patch('wave_view.core.plotter.SpiceData')
    def test_log_scale_preserves_data(self, mock_spice_data_class):
        """Test that applying log scale preserves original data values."""
        mock_spice_data_class.return_value = create_mock_spice_data()
        
        plotter = SpicePlotter("test.raw")
        plotter.load_config(create_log_scale_config())
        
        fig = plotter.create_figure()
        
        # Get the data from the trace
        trace_data = fig.data[0]
        
        # Check that X and Y data are preserved (log scale is layout only)
        expected_x = create_mock_spice_data().get_signal("frequency")
        expected_y = create_mock_spice_data().get_signal("v(out)")
        
        np.testing.assert_array_equal(trace_data.x, expected_x)
        np.testing.assert_array_equal(trace_data.y, expected_y)
    
    @patch('wave_view.core.plotter.SpiceData')
    def test_log_scale_multiple_traces(self, mock_spice_data_class):
        """Test log scale with multiple traces on same axis."""
        mock_spice_data_class.return_value = create_mock_spice_data()
        
        multi_trace_config = {
            "title": "Multi-trace Log Scale",
            "X": {"signal_key": "raw.frequency", "scale": "log"},
            "Y": [
                {
                    "label": "Signals",
                    "scale": "log",
                    "signals": {
                        "VDD": "v(vdd)",
                        "OUT": "v(out)",
                        "IDD": "i(vdd)"
                    }
                }
            ]
        }
        
        plotter = SpicePlotter("test.raw")
        plotter.load_config(multi_trace_config)
        
        fig = plotter.create_figure()
        
        # Check we have multiple traces
        self.assertEqual(len(fig.data), 3)
        
        # Check log scale applied to axis
        assert_log_scale_applied(fig.layout.xaxis, should_be_log=True)
        assert_log_scale_applied(fig.layout.yaxis, should_be_log=True)
        
        # Check all traces have same X data (frequency)
        expected_x = create_mock_spice_data().get_signal("frequency")
        for trace in fig.data:
            np.testing.assert_array_equal(trace.x, expected_x)


if __name__ == '__main__':
    unittest.main() 