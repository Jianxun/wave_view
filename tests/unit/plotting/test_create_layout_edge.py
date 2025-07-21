import pytest
import unittest

from yaml2plot.core.plotting import create_layout


class TestCreateLayoutEdgeCases(unittest.TestCase):
    """Edge-case verification for create_layout()."""

    def test_single_axis_defaults(self):
        cfg = {
            "x": {"signal": "time"},
            "y": [{"label": "Voltage", "signals": {"Out": "v(out)"}}],
        }
        layout = create_layout(cfg)

        # X-axis basic checks
        self.assertEqual(layout["xaxis"]["title"], "time")
        self.assertTrue(layout["xaxis"]["rangeslider"]["visible"])

        # Y-axis occupies full domain
        self.assertEqual(layout["yaxis"]["domain"], [0, 1])
        self.assertEqual(layout["yaxis"]["title"], "Voltage")

    def test_multi_axis_domain_order_and_gap(self):
        cfg = {
            "x": {"signal": "time"},
            "y": [
                {"label": "Top", "signals": {"A": "a"}},
                {"label": "Bottom", "signals": {"B": "b"}},
            ],
            "grid": False,  # disable grid globally
        }
        layout = create_layout(cfg)

        # Domains should be ordered top -> bottom with a gap in between
        top_dom = layout["yaxis"]["domain"]
        bottom_dom = layout["yaxis2"]["domain"]

        self.assertAlmostEqual(top_dom[1], 1.0)
        # bottom axis upper bound must be below top axis lower bound (gap)
        self.assertLess(bottom_dom[1], top_dom[0])
        # grid flag propagated
        self.assertFalse(layout["yaxis"]["showgrid"])
        self.assertFalse(layout["yaxis2"]["showgrid"])

    def test_log_scale_and_range_propagation(self):
        """Test that log scale and range are correctly propagated to layout."""
        # Test case 1: Log scale and range on X-axis and one Y-axis
        config = {
            "x": {"signal": "time", "scale": "log", "range": [1e-9, 1e-6]},
            "y": [
                {
                    "label": "Voltage",
                    "signals": {"V(out)": "v(out)"},
                    "scale": "log",
                    "range": [0.1, 1.2],
                },
                {"label": "Current", "signals": {"I(Vdd)": "i(vdd)"}},
            ],
        }

        layout = create_layout(config)

        # Verify X-axis
        self.assertEqual(layout["xaxis"]["type"], "log")
        self.assertEqual(layout["xaxis"]["range"], [1e-9, 1e-6])

        # Verify Y-axis 1
        self.assertEqual(layout["yaxis"]["type"], "log")
        self.assertEqual(layout["yaxis"]["range"], [0.1, 1.2])

        # Verify Y-axis 2 (no specific settings)
        self.assertEqual(layout["yaxis2"]["type"], "linear")
        self.assertNotIn("range", layout["yaxis2"])

    def test_linear_scale_and_no_range(self):
        """Test that linear scale and no range are default."""
        # Test case 2: Linear scale (default) and no range
        config = {
            "x": {"signal": "time"},
            "y": [
                {"label": "Voltage", "signals": {"V(out)": "v(out)"}},
                {"label": "Current", "signals": {"I(Vdd)": "i(vdd)"}},
            ],
        }

        layout = create_layout(config)

        # Verify X-axis
        self.assertEqual(layout["xaxis"]["type"], "linear")
        self.assertNotIn("range", layout["xaxis"])

        # Verify Y-axes
        self.assertEqual(layout["yaxis"]["type"], "linear")
        self.assertNotIn("range", layout["yaxis"])
        self.assertEqual(layout["yaxis2"]["type"], "linear")
        self.assertNotIn("range", layout["yaxis2"])

    def test_disable_rangeslider(self):
        cfg = {
            "x": {"signal": "time"},
            "y": [
                {"label": "Voltage", "signals": {"Out": "v(out)"}},
            ],
            "show_rangeslider": False,
        }
        layout = create_layout(cfg)
        self.assertFalse(layout["xaxis"]["rangeslider"]["visible"])


class TestSIEngineeringNotationEdgeCases(unittest.TestCase):
    """Tests for SI engineering notation applied to all axes."""

    def test_x_axis_always_uses_si_notation(self):
        """All X-axes should use SI engineering notation for consistent formatting."""
        config = {
            "title": "Frequency Response",
            "x": {"signal": "frequency", "label": "Frequency (Hz)", "scale": "log"},
            "y": [{"label": "Magnitude (dB)", "signals": {"Output": "v(out)"}}],
        }

        layout = create_layout(config)

        # SI engineering notation should be enabled for all X-axes
        self.assertEqual(layout["xaxis"]["exponentformat"], "SI")
        self.assertEqual(layout["xaxis"]["type"], "log")
        self.assertEqual(layout["xaxis"]["title"], "Frequency (Hz)")

    def test_time_domain_x_axis_uses_si_notation(self):
        """Time domain X-axis should also use SI engineering notation."""
        config = {
            "title": "Time Domain Analysis",
            "x": {"signal": "time", "label": "Time (s)", "scale": "linear"},
            "y": [{"label": "Voltage (V)", "signals": {"Output": "v(out)"}}],
        }

        layout = create_layout(config)

        # SI engineering notation should be enabled for all signals
        self.assertEqual(layout["xaxis"]["exponentformat"], "SI")
        self.assertEqual(layout["xaxis"]["title"], "Time (s)")

    def test_y_axes_use_si_notation(self):
        """All Y-axes should use SI engineering notation."""
        config = {
            "title": "Multi-Axis Analysis",
            "x": {"signal": "time", "label": "Time (s)", "scale": "linear"},
            "y": [
                {"label": "Voltage (V)", "signals": {"Output": "v(out)"}},
                {"label": "Current (A)", "signals": {"Input": "i(in)"}},
            ],
        }

        layout = create_layout(config)

        # SI engineering notation should be enabled for all Y-axes
        self.assertEqual(layout["yaxis"]["exponentformat"], "SI")
        self.assertEqual(layout["yaxis2"]["exponentformat"], "SI")
        self.assertEqual(layout["yaxis"]["title"], "Voltage (V)")
        self.assertEqual(layout["yaxis2"]["title"], "Current (A)")
