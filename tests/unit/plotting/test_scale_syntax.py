"""
Test both intuitive and legacy scale syntax support.
"""

import unittest
from yaml2plot.core.plotting import create_layout


class TestScaleSyntax(unittest.TestCase):
    """Test that axes support scale: 'log'."""

    def test_x_axis_scale(self):
        """Test X-axis scale setting."""
        config = {"x": {"signal": "frequency", "scale": "log"}}
        layout = create_layout(config)
        self.assertEqual(layout["xaxis"]["type"], "log")

    def test_y_axis_scale(self):
        """Test Y-axis scale setting."""
        y_spec = {"label": "Voltage", "signals": {"V": "v(out)"}, "scale": "log"}
        config = {"x": {"signal": "time"}, "y": [y_spec]}
        layout = create_layout(config)
        self.assertEqual(layout["yaxis"]["type"], "log")

    def test_default_linear_scale(self):
        """Test that scale defaults to linear."""
        config = {
            "x": {"signal": "time"},
            "y": [{"label": "V", "signals": {"V": "v(out)"}}],
        }
        layout = create_layout(config)
        self.assertEqual(layout["xaxis"]["type"], "linear")
        self.assertEqual(layout["yaxis"]["type"], "linear")
