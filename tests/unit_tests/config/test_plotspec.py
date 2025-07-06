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
    import plotly.graph_objects as go
except ImportError:
    PlotSpec = None
    YAxisSpec = None
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



 


class TestPlotSpecV1_0_0_NewMethods(unittest.TestCase):
    """Test PlotSpec v1.0.0 new methods - configuration-only functionality."""
    
    def test_plotspec_to_dict_method_returns_clean_config(self):
        """Test that PlotSpec.to_dict() returns clean configuration dict for v1.0.0 plotting functions."""
        # Skip test if PlotSpec not implemented yet
        if PlotSpec is None:
            self.skipTest("PlotSpec not implemented yet")
        
        # Create a PlotSpec with comprehensive configuration
        spec = PlotSpec.from_yaml("""
title: "Test Plot"
x: "time"
y:
  - label: "Voltages (V)"
    signals:
      Input: "v(in)"
      Output: "v(out)"
    log_scale: false
    unit: "V"
    range: [0, 3.3]
    color: "blue"
  - label: "Current (A)"
    signals:
      Supply: "i(vdd)"
    log_scale: true
    unit: "A"

width: 1200
height: 800
theme: "plotly_dark"
title_x: 0.5
title_xanchor: "center"
show_legend: true
grid: true
zoom_buttons: false
zoom_buttons_x: 0.1
zoom_buttons_y: 1.1
show_rangeslider: false
""")
        
        # Call the to_dict() method - this should fail initially (TDD Red phase)
        config_dict = spec.to_dict()
        
        # Verify the returned dictionary has the expected structure
        self.assertIsInstance(config_dict, dict)
        
        # Verify basic structure
        self.assertEqual(config_dict["title"], "Test Plot")
        self.assertEqual(config_dict["x"], "time")
        self.assertIsInstance(config_dict["y"], list)
        self.assertEqual(len(config_dict["y"]), 2)
        
        # Verify first Y-axis configuration
        y1 = config_dict["y"][0]
        self.assertEqual(y1["label"], "Voltages (V)")
        self.assertEqual(y1["signals"], {"Input": "v(in)", "Output": "v(out)"})
        self.assertEqual(y1["log_scale"], False)
        self.assertEqual(y1["unit"], "V")
        self.assertEqual(y1["range"], [0, 3.3])
        self.assertEqual(y1["color"], "blue")
        
        # Verify second Y-axis configuration
        y2 = config_dict["y"][1]
        self.assertEqual(y2["label"], "Current (A)")
        self.assertEqual(y2["signals"], {"Supply": "i(vdd)"})
        self.assertEqual(y2["log_scale"], True)
        self.assertEqual(y2["unit"], "A")
        self.assertIsNone(y2.get("range"))  # Not specified, should be None
        self.assertIsNone(y2.get("color"))  # Not specified, should be None
        
        # Verify styling options
        self.assertEqual(config_dict["width"], 1200)
        self.assertEqual(config_dict["height"], 800)
        self.assertEqual(config_dict["theme"], "plotly_dark")
        self.assertEqual(config_dict["title_x"], 0.5)
        self.assertEqual(config_dict["title_xanchor"], "center")
        self.assertEqual(config_dict["show_legend"], True)
        self.assertEqual(config_dict["grid"], True)
        self.assertEqual(config_dict["zoom_buttons"], False)
        self.assertEqual(config_dict["zoom_buttons_x"], 0.1)
        self.assertEqual(config_dict["zoom_buttons_y"], 1.1)
        self.assertEqual(config_dict["show_rangeslider"], False)

    def test_plotspec_to_dict_with_minimal_config(self):
        """Test to_dict() with minimal configuration and default values."""
        # Skip test if PlotSpec not implemented yet
        if PlotSpec is None:
            self.skipTest("PlotSpec not implemented yet")
        
        # Create minimal PlotSpec
        spec = PlotSpec.from_yaml("""
x: "time"
y:
  - label: "Voltage"
    signals:
      Output: "v(out)"
""")
        
        # Call to_dict() method
        config_dict = spec.to_dict()
        
        # Verify minimal structure
        self.assertEqual(config_dict["x"], "time")
        self.assertEqual(len(config_dict["y"]), 1)
        
        # Verify Y-axis with minimal config
        y1 = config_dict["y"][0]
        self.assertEqual(y1["label"], "Voltage")
        self.assertEqual(y1["signals"], {"Output": "v(out)"})
        self.assertEqual(y1["log_scale"], False)  # Default value
        self.assertIsNone(y1.get("unit"))  # Default None
        self.assertIsNone(y1.get("range"))  # Default None
        self.assertIsNone(y1.get("color"))  # Default None
        
        # Verify default styling options
        self.assertIsNone(config_dict.get("title"))  # Default None
        self.assertIsNone(config_dict.get("width"))  # Default None
        self.assertIsNone(config_dict.get("height"))  # Default None
        self.assertEqual(config_dict["theme"], "plotly")  # Default value
        self.assertEqual(config_dict["title_x"], 0.5)  # Default value
        self.assertEqual(config_dict["title_xanchor"], "center")  # Default value
        self.assertEqual(config_dict["show_legend"], True)  # Default value
        self.assertEqual(config_dict["grid"], True)  # Default value
        self.assertEqual(config_dict["zoom_buttons"], True)  # Default value 