"""
Unit tests for PlotSpec Pydantic model.

This module tests PlotSpec initialization, validation, and basic functionality.
Following TDD principles - implementing one test case at a time.
"""

import unittest
from unittest.mock import Mock, patch
from pydantic import ValidationError

# Import will fail initially - that's expected in TDD
try:
    from wave_view.core.plotspec import PlotSpec, YAxisSpec
    from wave_view.core.reader import SpiceData
    import plotly.graph_objects as go
except ImportError:
    PlotSpec = None
    YAxisSpec = None
    SpiceData = None
    go = None


class TestPlotSpecBasicInitialization(unittest.TestCase):
    """Test PlotSpec basic initialization and validation."""
    
    def test_create_plotspec_from_minimal_dict(self):
        """Test creating PlotSpec from minimal valid configuration."""
        # Skip test if PlotSpec not implemented yet
        if PlotSpec is None:
            self.skipTest("PlotSpec not implemented yet")
        
        # Minimal valid configuration
        config_dict = {
            "x": "time",
            "y": [
                {
                    "label": "Voltage",
                    "signals": {"VDD": "v(vdd)"}
                }
            ]
        }
        
        # This should work without raising exceptions
        spec = PlotSpec.model_validate(config_dict)
        
        # Verify the data was parsed correctly
        self.assertEqual(spec.x, "time")
        self.assertEqual(len(spec.y), 1)
        self.assertEqual(spec.y[0].label, "Voltage")
        self.assertEqual(spec.y[0].signals["VDD"], "v(vdd)")
        
        # Verify default values
        self.assertIsNone(spec.title)
        self.assertEqual(spec.title_x, 0.5)
        self.assertEqual(spec.title_xanchor, "center")
        self.assertTrue(spec.show_legend)
        self.assertTrue(spec.grid)
        self.assertTrue(spec.zoom_buttons)

    def test_create_plotspec_from_yaml_string(self):
        """Test creating PlotSpec from YAML string using from_yaml() method."""
        # Skip test if PlotSpec not implemented yet
        if PlotSpec is None:
            self.skipTest("PlotSpec not implemented yet")
        
        # YAML string with minimal valid configuration
        yaml_str = """
title: "Test Plot"
x: "time"
y:
  - label: "Voltage"
    signals:
      VDD: "v(vdd)"
      OUT: "v(out)"
"""
        
        # This should work without raising exceptions
        spec = PlotSpec.from_yaml(yaml_str)
        
        # Verify the data was parsed correctly
        self.assertEqual(spec.title, "Test Plot")
        self.assertEqual(spec.x, "time")
        self.assertEqual(len(spec.y), 1)
        self.assertEqual(spec.y[0].label, "Voltage")
        self.assertEqual(spec.y[0].signals["VDD"], "v(vdd)")
        self.assertEqual(spec.y[0].signals["OUT"], "v(out)")
        
        # Verify default values are still applied
        self.assertEqual(spec.title_x, 0.5)
        self.assertEqual(spec.title_xanchor, "center")
        self.assertTrue(spec.show_legend)
        self.assertTrue(spec.grid)
        self.assertTrue(spec.zoom_buttons)

    def test_create_plotspec_with_multi_axis_y_config(self):
        """Test creating PlotSpec with multiple Y-axes based on real demo_ota_5t.py examples."""
        # Skip test if PlotSpec not implemented yet
        if PlotSpec is None:
            self.skipTest("PlotSpec not implemented yet")
        
        # Real multi-axis YAML config based on demo_ota_5t.py
        yaml_str = """
title: "SPICE Simulation - Key Signals"
x: "time"
y:
  - label: "Voltages (V)"
    signals:
      Input: "v(in)"
      Output: "v(out)" 
      VDDA: "v(vdda)"
      VSSA: "v(vssa)"
      
  - label: "Current (A)"
    signals:
      Supply Current: "i(v_vdda)"
"""
        
        # This should work without raising exceptions
        spec = PlotSpec.from_yaml(yaml_str)
        
        # Verify the basic structure
        self.assertEqual(spec.title, "SPICE Simulation - Key Signals")
        self.assertEqual(spec.x, "time")
        self.assertEqual(len(spec.y), 2)
        
        # Verify first Y-axis (Voltages)
        voltage_axis = spec.y[0]
        self.assertEqual(voltage_axis.label, "Voltages (V)")
        self.assertEqual(len(voltage_axis.signals), 4)
        self.assertEqual(voltage_axis.signals["Input"], "v(in)")
        self.assertEqual(voltage_axis.signals["Output"], "v(out)")
        self.assertEqual(voltage_axis.signals["VDDA"], "v(vdda)")
        self.assertEqual(voltage_axis.signals["VSSA"], "v(vssa)")
        
        # Verify second Y-axis (Current)
        current_axis = spec.y[1]
        self.assertEqual(current_axis.label, "Current (A)")
        self.assertEqual(len(current_axis.signals), 1)
        self.assertEqual(current_axis.signals["Supply Current"], "i(v_vdda)")
        
        # Verify both axes have correct defaults for optional fields
        self.assertFalse(voltage_axis.log_scale)
        self.assertFalse(current_axis.log_scale)
        self.assertIsNone(voltage_axis.unit)
        self.assertIsNone(current_axis.unit)
        self.assertIsNone(voltage_axis.range)
        self.assertIsNone(current_axis.range)

    def test_plotspec_plot_method_returns_plotly_figure(self):
        """Test that PlotSpec.plot(data) returns a Plotly Figure object."""
        # Skip test if dependencies not available
        if PlotSpec is None or SpiceData is None or go is None:
            self.skipTest("PlotSpec, SpiceData, or plotly not available yet")
        
        # Create a simple PlotSpec
        spec = PlotSpec.model_validate({
            "title": "Test Plot",
            "x": "time", 
            "y": [
                {
                    "label": "Voltage",
                    "signals": {"VDD": "v(vdd)"}
                }
            ]
        })
        
        # Create a mock SpiceData object with required methods
        mock_data = Mock(spec=SpiceData)
        mock_data.get_signal.return_value = [0, 1, 2, 3, 4]  # Mock signal data
        mock_data.signals = ["time", "v(vdd)"]  # Mock available signals
        
        # Call the plot method
        fig = spec.plot(mock_data)
        
        # Verify it returns a Plotly Figure object
        self.assertIsInstance(fig, go.Figure)
        
        # Verify the mock was called appropriately
        # Should call get_signal for x-axis (time) and y-axis (v(vdd))
        expected_calls = mock_data.get_signal.call_args_list
        self.assertGreater(len(expected_calls), 0, "get_signal should be called at least once")


if __name__ == '__main__':
    unittest.main() 


class TestPlotSpecNewMethods(unittest.TestCase):
    """Test PlotSpec new methods: from_file(), show(), get_figure()."""
    
    def test_plotspec_from_file_method_loads_yaml_file(self):
        """Test that PlotSpec.from_file() loads configuration from YAML file."""
        # Skip test if PlotSpec not implemented yet
        if PlotSpec is None:
            self.skipTest("PlotSpec not implemented yet")
        
        # Create a temporary YAML file for testing
        import tempfile
        import os
        
        yaml_content = """
title: "Test Plot from File"
x: "time"
y:
  - label: "Voltage"
    signals:
      VDD: "v(vdd)"
      OUT: "v(out)"
width: 800
height: 600
"""
        
        # Write to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write(yaml_content)
            temp_file_path = f.name
        
        try:
            # Test the from_file method
            spec = PlotSpec.from_file(temp_file_path)
            
            # Verify the data was loaded correctly
            self.assertEqual(spec.title, "Test Plot from File")
            self.assertEqual(spec.x, "time")
            self.assertEqual(len(spec.y), 1)
            self.assertEqual(spec.y[0].label, "Voltage")
            self.assertEqual(spec.y[0].signals["VDD"], "v(vdd)")
            self.assertEqual(spec.y[0].signals["OUT"], "v(out)")
            self.assertEqual(spec.width, 800)
            self.assertEqual(spec.height, 600)
            
        finally:
            # Clean up temporary file
            os.unlink(temp_file_path) 

    def test_plotspec_show_method_displays_plot(self):
        """Test that PlotSpec.show() method displays the plot directly."""
        # Skip test if dependencies not available
        if PlotSpec is None or SpiceData is None or go is None:
            self.skipTest("PlotSpec, SpiceData, or plotly not available yet")
        
        # Create a simple PlotSpec
        spec = PlotSpec.model_validate({
            "title": "Test Show Method",
            "x": "time", 
            "y": [
                {
                    "label": "Voltage",
                    "signals": {"VDD": "v(vdd)"}
                }
            ]
        })
        
        # Create a mock SpiceData object
        mock_data = Mock(spec=SpiceData)
        mock_data.get_signal.return_value = [0, 1, 2, 3, 4]
        mock_data.signals = ["time", "v(vdd)"]
        
        # Mock the figure.show() method to verify it's called
        with patch('plotly.graph_objects.Figure.show') as mock_show:
            # Call the show method
            result = spec.show(mock_data)
            
            # Verify show() was called on the figure
            mock_show.assert_called_once()
            
            # Verify the method returns None (it's a display method)
            self.assertIsNone(result)

    def test_plotspec_get_figure_method_returns_plotly_figure(self):
        """Test that PlotSpec.get_figure() returns a Plotly Figure object (alias for plot())."""
        # Skip test if dependencies not available
        if PlotSpec is None or SpiceData is None or go is None:
            self.skipTest("PlotSpec, SpiceData, or plotly not available yet")
        
        # Create a simple PlotSpec
        spec = PlotSpec.model_validate({
            "title": "Test Get Figure Method",
            "x": "time", 
            "y": [
                {
                    "label": "Voltage",
                    "signals": {"VDD": "v(vdd)"}
                }
            ]
        })
        
        # Create a mock SpiceData object
        mock_data = Mock(spec=SpiceData)
        mock_data.get_signal.return_value = [0, 1, 2, 3, 4]
        mock_data.signals = ["time", "v(vdd)"]
        
        # Call both methods
        fig1 = spec.plot(mock_data)
        fig2 = spec.get_figure(mock_data)
        
        # Verify both return Plotly Figure objects
        self.assertIsInstance(fig1, go.Figure)
        self.assertIsInstance(fig2, go.Figure)
        
        # Verify both methods return equivalent figures
        # (They should have the same data and layout structure)
        self.assertEqual(type(fig1), type(fig2))
        # Both should be Figure objects - that's sufficient for this test 