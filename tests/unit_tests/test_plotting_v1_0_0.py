"""
Unit tests for v1.0.0 plotting functions.

This module tests the new standalone plotting functions that work with
Dict[str, np.ndarray] data and PlotSpec configuration.
Following TDD principles - implementing one test case at a time.
"""

import unittest
import numpy as np
import plotly.graph_objects as go
import pytest

# Import will fail initially - that's expected in TDD
try:
    from wave_view.core.plotting import plot, create_figure, create_layout, add_waveform
    from wave_view.core.plotspec import PlotSpec
except ImportError:
    plot = None
    create_figure = None
    create_layout = None
    add_waveform = None
    PlotSpec = None


class TestPlottingFunctionsBasic(unittest.TestCase):
    """Test basic plotting functions for v1.0.0 architecture."""
    
    def setUp(self):
        """Set up test data for plotting tests."""
        # Create simple test data
        self.test_data = {
            "time": np.linspace(0, 1, 100),
            "v(out)": np.sin(2 * np.pi * 5 * np.linspace(0, 1, 100)),
            "v(in)": np.cos(2 * np.pi * 5 * np.linspace(0, 1, 100)),
            "i(vdd)": 0.001 * np.sin(2 * np.pi * 5 * np.linspace(0, 1, 100))
        }
    
    def test_plot_function_creates_figure_from_data_and_spec(self):
        """Test that plot() function creates Plotly figure from data dict and PlotSpec."""
        # Skip test if functions not implemented yet
        if plot is None or PlotSpec is None:
            self.skipTest("Plotting functions not implemented yet")
        
        # Create simple PlotSpec
        spec = PlotSpec.from_yaml("""
x: "time"
y:
  - label: "Voltage"
    signals:
      Output: "v(out)"
      Input: "v(in)"
""")
        
        # Call the plot function - this should fail initially (TDD Red phase)
        fig = plot(self.test_data, spec)
        
        # Verify the returned object is a Plotly figure
        self.assertIsInstance(fig, go.Figure)
        
        # Verify the figure has the expected traces
        self.assertEqual(len(fig.data), 2)  # Two signals
        
        # Verify trace names
        trace_names = [trace.name for trace in fig.data]
        self.assertIn("Output", trace_names)
        self.assertIn("Input", trace_names)
        
        # Verify X-axis data
        for trace in fig.data:
            np.testing.assert_array_equal(trace.x, self.test_data["time"])
        
        # Verify Y-axis data
        output_trace = next(trace for trace in fig.data if trace.name == "Output")
        np.testing.assert_array_equal(output_trace.y, self.test_data["v(out)"])
        
        input_trace = next(trace for trace in fig.data if trace.name == "Input")
        np.testing.assert_array_equal(input_trace.y, self.test_data["v(in)"])

    def test_plot_function_handles_multi_axis_configuration(self):
        """Test plot() function with multi-axis Y configuration."""
        # Skip test if functions not implemented yet
        if plot is None or PlotSpec is None:
            self.skipTest("Plotting functions not implemented yet")
        
        # Create multi-axis PlotSpec
        spec = PlotSpec.from_yaml("""
title: "Multi-Axis Test"
x: "time"
y:
  - label: "Voltages (V)"
    signals:
      Output: "v(out)"
      Input: "v(in)"
  - label: "Current (A)"
    signals:
      Supply: "i(vdd)"
""")
        
        # Call the plot function
        fig = plot(self.test_data, spec)
        
        # Verify the returned object is a Plotly figure
        self.assertIsInstance(fig, go.Figure)
        
        # Verify the figure has the expected traces
        self.assertEqual(len(fig.data), 3)  # Three signals total
        
        # Verify trace names
        trace_names = [trace.name for trace in fig.data]
        self.assertIn("Output", trace_names)
        self.assertIn("Input", trace_names)
        self.assertIn("Supply", trace_names)
        
        # Verify Y-axis assignments
        # First Y-axis traces should use 'y' (default)
        voltage_traces = [trace for trace in fig.data if trace.name in ["Output", "Input"]]
        for trace in voltage_traces:
            self.assertEqual(trace.yaxis, "y")
        
        # Second Y-axis traces should use 'y2'
        current_traces = [trace for trace in fig.data if trace.name == "Supply"]
        for trace in current_traces:
            self.assertEqual(trace.yaxis, "y2")

    def test_plot_function_applies_basic_styling(self):
        """Test plot() function applies basic styling from PlotSpec."""
        # Skip test if functions not implemented yet
        if plot is None or PlotSpec is None:
            self.skipTest("Plotting functions not implemented yet")
        
        # Create PlotSpec with styling
        spec = PlotSpec.from_yaml("""
title: "Styled Plot"
x: "time"
y:
  - label: "Voltage"
    signals:
      Output: "v(out)"
width: 1000
height: 600
theme: "plotly_dark"
show_legend: false
""")
        
        # Call the plot function
        fig = plot(self.test_data, spec)
        
        # Verify styling was applied
        self.assertEqual(fig.layout.title.text, "Styled Plot")
        self.assertEqual(fig.layout.width, 1000)
        self.assertEqual(fig.layout.height, 600)
        # Template is set (exact comparison is complex due to Plotly's template structure)
        self.assertIsNotNone(fig.layout.template)
        self.assertEqual(fig.layout.showlegend, False)


class TestPlottingHelperFunctions(unittest.TestCase):
    """Test helper functions for plotting."""
    
    def test_create_figure_returns_empty_plotly_figure(self):
        """Test that create_figure() returns empty Plotly figure."""
        # Skip test if functions not implemented yet
        if create_figure is None:
            self.skipTest("Helper functions not implemented yet")
        
        # Call create_figure
        fig = create_figure()
        
        # Verify it returns a Plotly figure
        self.assertIsInstance(fig, go.Figure)
        
        # Verify it's empty (no traces)
        self.assertEqual(len(fig.data), 0)

    def test_create_layout_returns_layout_dict(self):
        """Test that create_layout() returns proper layout configuration."""
        # Skip test if functions not implemented yet
        if create_layout is None:
            self.skipTest("Helper functions not implemented yet")
        
        # Test config
        config = {
            "title": "Test Plot",
            "width": 800,
            "height": 400,
            "x": "time",
            "y": [
                {"label": "Voltage", "signals": {"Out": "v(out)"}},
                {"label": "Current", "signals": {"Supply": "i(vdd)"}}
            ]
        }
        
        # Call create_layout
        layout = create_layout(config)
        
        # Verify it returns a dict
        self.assertIsInstance(layout, dict)
        
        # Verify basic layout properties
        self.assertEqual(layout["title"]["text"], "Test Plot")
        self.assertEqual(layout["width"], 800)
        self.assertEqual(layout["height"], 400)
        
        # Verify axes are configured
        self.assertIn("xaxis", layout)
        self.assertIn("yaxis", layout)
        self.assertIn("yaxis2", layout)  # Second Y-axis

    def test_add_waveform_adds_trace_to_figure(self):
        """Test that add_waveform() adds trace to figure."""
        # Skip test if functions not implemented yet
        if add_waveform is None or create_figure is None:
            self.skipTest("Helper functions not implemented yet")
        
        # Create test data
        x_data = np.linspace(0, 1, 10)
        y_data = np.sin(2 * np.pi * x_data)
        
        # Create empty figure
        fig = create_figure()
        
        # Add waveform
        add_waveform(fig, x_data, y_data, name="Test Signal")
        
        # Verify trace was added
        self.assertEqual(len(fig.data), 1)
        
        # Verify trace properties
        trace = fig.data[0]
        self.assertEqual(trace.name, "Test Signal")
        np.testing.assert_array_equal(trace.x, x_data)
        np.testing.assert_array_equal(trace.y, y_data)

    def test_add_waveform_with_y_axis_specification(self):
        """Test add_waveform() with Y-axis specification."""
        # Skip test if functions not implemented yet
        if add_waveform is None or create_figure is None:
            self.skipTest("Helper functions not implemented yet")
        
        # Create test data
        x_data = np.linspace(0, 1, 10)
        y_data = np.sin(2 * np.pi * x_data)
        
        # Create empty figure
        fig = create_figure()
        
        # Add waveform to second Y-axis
        add_waveform(fig, x_data, y_data, name="Test Signal", y_axis="y2")
        
        # Verify trace was added with correct Y-axis
        self.assertEqual(len(fig.data), 1)
        trace = fig.data[0]
        self.assertEqual(trace.yaxis, "y2")

    @pytest.mark.skip(reason="Zoom buttons feature removed in v1.0.0")
    def test_create_layout_with_zoom_buttons(self):
        """Test create_layout with zoom buttons enabled."""
        if create_layout is None:
            self.skipTest("Helper functions not implemented yet")
        
        config = {
            "title": "Test Plot with Zoom Buttons",
            "x": "time",
            "y": [
                {
                    "label": "Voltage (V)",
                    "signals": {"VDD": "v(vdd)"}
                }
            ],
            "zoom_buttons": True,
            "zoom_buttons_x": 0.1,
            "zoom_buttons_y": 1.1
        }
        
        layout = create_layout(config)
        
        # Test zoom buttons configuration
        self.assertIn("updatemenus", layout)
        self.assertEqual(len(layout["updatemenus"]), 1)
        
        menu = layout["updatemenus"][0]
        self.assertEqual(menu["type"], "buttons")
        self.assertEqual(menu["direction"], "right")
        self.assertEqual(menu["x"], 0.1)
        self.assertEqual(menu["y"], 1.1)
        self.assertEqual(menu["showactive"], True)
        
        # Test zoom buttons
        buttons = menu["buttons"]
        self.assertEqual(len(buttons), 3)
        self.assertEqual(buttons[0]["label"], "Zoom XY")
        self.assertEqual(buttons[1]["label"], "Zoom Y")
        self.assertEqual(buttons[2]["label"], "Zoom X")
        
        # Test zoom button arguments
        xy_args = buttons[0]["args"][0]
        self.assertEqual(xy_args["dragmode"], "zoom")
        self.assertEqual(xy_args["xaxis.fixedrange"], False)
        self.assertEqual(xy_args["yaxis.fixedrange"], False)
        
        y_args = buttons[1]["args"][0]
        self.assertEqual(y_args["dragmode"], "zoom")
        self.assertEqual(y_args["xaxis.fixedrange"], True)
        self.assertEqual(y_args["yaxis.fixedrange"], False)
        
        x_args = buttons[2]["args"][0]
        self.assertEqual(x_args["dragmode"], "zoom")
        self.assertEqual(x_args["xaxis.fixedrange"], False)
        self.assertEqual(x_args["yaxis.fixedrange"], True)

    @pytest.mark.skip(reason="Zoom buttons feature removed in v1.0.0")
    def test_create_layout_with_zoom_buttons_multi_axis(self):
        """Test create_layout with zoom buttons and multiple Y-axes."""
        if create_layout is None:
            self.skipTest("Helper functions not implemented yet")
        
        config = {
            "title": "Multi-Axis Plot with Zoom Buttons",
            "x": "time",
            "y": [
                {
                    "label": "Voltage (V)",
                    "signals": {"VDD": "v(vdd)"}
                },
                {
                    "label": "Current (A)",
                    "signals": {"IDD": "i(vdd)"}
                }
            ],
            "zoom_buttons": True
        }
        
        layout = create_layout(config)
        
        # Test zoom buttons with multiple Y-axes
        self.assertIn("updatemenus", layout)
        menu = layout["updatemenus"][0]
        buttons = menu["buttons"]
        
        # Test that zoom buttons handle multiple Y-axes
        xy_args = buttons[0]["args"][0]
        self.assertIn("yaxis.fixedrange", xy_args)
        self.assertIn("yaxis2.fixedrange", xy_args)
        
        y_args = buttons[1]["args"][0]
        self.assertIn("yaxis.fixedrange", y_args)
        self.assertIn("yaxis2.fixedrange", y_args)
        
        x_args = buttons[2]["args"][0]
        self.assertIn("yaxis.fixedrange", x_args)
        self.assertIn("yaxis2.fixedrange", x_args)

    def test_create_layout_without_zoom_buttons(self):
        """Test create_layout() without zoom buttons enabled."""
        if create_layout is None:
            self.skipTest("Helper functions not implemented yet")
        
        config = {
            "title": "No Zoom Buttons",
            "x": "time",
            "y": [{"label": "Voltage", "signals": {"Out": "v(out)"}}],
            "zoom_buttons": False  # Explicitly disabled
        }
        
        layout = create_layout(config)
        
        # Verify no zoom buttons configuration
        self.assertNotIn("updatemenus", layout)

    @pytest.mark.skip(reason="Zoom buttons feature removed in v1.0.0")
    def test_zoom_xy_mode_settings_verification(self):
        """Test to verify the exact settings of Zoom XY mode work correctly."""
        if create_layout is None:
            self.skipTest("Helper functions not implemented yet")
        
        # Test with multi-axis to verify all axes are configured
        config = {
            "title": "Zoom XY Test",
            "x": "time",
            "y": [
                {"label": "Voltage", "signals": {"Out": "v(out)"}},
                {"label": "Current", "signals": {"Supply": "i(vdd)"}},
                {"label": "Power", "signals": {"Power": "p(load)"}}
            ],
            "zoom_buttons": True
        }
        
        layout = create_layout(config)
        
        # Verify zoom buttons are present
        self.assertIn("updatemenus", layout)
        buttons = layout["updatemenus"][0]["buttons"]
        
        # Find the Zoom XY button
        zoom_xy_button = next((btn for btn in buttons if btn["label"] == "Zoom XY"), None)
        self.assertIsNotNone(zoom_xy_button, "Zoom XY button should exist")
        
        # Extract the exact settings
        zoom_xy_args = zoom_xy_button["args"][0]
        
        # Verify the exact settings we want to make default
        expected_settings = {
            "dragmode": "zoom",
            "xaxis.fixedrange": False,
            "yaxis.fixedrange": False,
            "yaxis2.fixedrange": False,
            "yaxis3.fixedrange": False
        }
        
        for key, expected_value in expected_settings.items():
            self.assertEqual(zoom_xy_args.get(key), expected_value, 
                           f"Setting '{key}' should be {expected_value}")
        
        # Verify these are the optimal settings for default behavior
        self.assertEqual(zoom_xy_args["dragmode"], "zoom")
        self.assertFalse(zoom_xy_args["xaxis.fixedrange"])
        self.assertFalse(zoom_xy_args["yaxis.fixedrange"])
        self.assertFalse(zoom_xy_args["yaxis2.fixedrange"])
        self.assertFalse(zoom_xy_args["yaxis3.fixedrange"])

    def test_y_axis_domain_ordering_matches_yaml_order(self):
        """Test that Y-axis domains are ordered correctly - first axis at top."""
        if create_layout is None:
            self.skipTest("Helper functions not implemented yet")
        
        # Test with 3 Y-axes to verify domain ordering
        config = {
            "title": "Y-Axis Ordering Test",
            "x": "time",
            "y": [
                {"label": "First (Top)", "signals": {"Signal1": "v(out)"}},
                {"label": "Second (Middle)", "signals": {"Signal2": "i(vdd)"}},
                {"label": "Third (Bottom)", "signals": {"Signal3": "p(load)"}}
            ]
        }
        
        layout = create_layout(config)
        
        # Verify Y-axis domains are ordered correctly
        # First axis (yaxis) should be at the top
        first_domain = layout["yaxis"]["domain"]
        second_domain = layout["yaxis2"]["domain"]
        third_domain = layout["yaxis3"]["domain"]
        
        # Verify ordering: first axis at top, third axis at bottom
        self.assertGreater(first_domain[0], second_domain[0], 
                          "First axis should be higher than second axis")
        self.assertGreater(first_domain[1], second_domain[1], 
                          "First axis should be higher than second axis")
        
        self.assertGreater(second_domain[0], third_domain[0], 
                          "Second axis should be higher than third axis")
        self.assertGreater(second_domain[1], third_domain[1], 
                          "Second axis should be higher than third axis")
        
        # Verify first axis is at the top (domain[1] close to 1.0)
        self.assertGreater(first_domain[1], 0.9, 
                          "First axis should be near the top of the figure")
        
        # Verify third axis is at the bottom (domain[0] close to 0.0)
        self.assertLess(third_domain[0], 0.1, 
                       "Third axis should be near the bottom of the figure")


if __name__ == '__main__':
    unittest.main() 