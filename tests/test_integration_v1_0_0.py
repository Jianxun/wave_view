"""
Integration tests for v1.0.0 API.

Tests the complete workflow of the v1.0.0 architecture:
Dict[str, np.ndarray] data → PlotSpec → plot() → Figure
"""

import unittest
import numpy as np
import plotly.graph_objects as go
import wave_view as wv
from pathlib import Path


class TestV1_0_0Integration(unittest.TestCase):
    """Integration tests for v1.0.0 plot function."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_raw_file = Path("tests/raw_files/Ring_Oscillator_7stage.raw")
        self.assertTrue(self.test_raw_file.exists(), f"Test file not found: {self.test_raw_file}")

    def test_v1_0_0_plot_with_real_data(self):
        """Test v1.0.0 plot function with real SPICE data."""
        # Load real SPICE data using v1.0.0 loader
        data, _ = wv.load_spice_raw(self.test_raw_file)
        
        # Create PlotSpec configuration using actual signal names
        spec = wv.PlotSpec.from_yaml("""
title: "Ring Oscillator - v1.0.0 Test"
x: "time"
y:
  - label: "Voltages (V)"
    signals:
      VDD: "v(vdd)"
      Bus01: "v(bus01)"
""")
        
        # Call v1.0.0 plot function
        fig = wv.plot(data, spec, show=False)
        
        # Verify the result
        self.assertIsInstance(fig, go.Figure)
        self.assertEqual(len(fig.data), 2)  # 2 traces
        
        # Check traces
        self.assertEqual(fig.data[0].name, "VDD")
        self.assertEqual(fig.data[1].name, "Bus01")
        
        # Check layout
        self.assertEqual(fig.layout.title.text, "Ring Oscillator - v1.0.0 Test")
        self.assertEqual(fig.layout.xaxis.title.text, "time")
        self.assertEqual(fig.layout.yaxis.title.text, "Voltages (V)")
        
        # Check data arrays
        self.assertIsInstance(fig.data[0].x, np.ndarray)
        self.assertIsInstance(fig.data[0].y, np.ndarray)
        self.assertIsInstance(fig.data[1].x, np.ndarray) 
        self.assertIsInstance(fig.data[1].y, np.ndarray)
        
        # Check that data is not empty
        self.assertGreater(len(fig.data[0].x), 0)
        self.assertGreater(len(fig.data[0].y), 0)
        self.assertGreater(len(fig.data[1].x), 0)
        self.assertGreater(len(fig.data[1].y), 0)
        
        print("✅ v1.0.0 plot() function working correctly with real data")

    def test_v1_0_0_plot_with_multi_axis(self):
        """Test v1.0.0 plot function with multi-axis configuration."""
        # Load real SPICE data
        data, _ = wv.load_spice_raw(self.test_raw_file)
        
        # Create multi-axis PlotSpec using actual signal names
        spec = wv.PlotSpec.from_yaml("""
title: "Ring Oscillator - Multi-Axis Test"
x: "time"
y:
  - label: "Supply Voltage (V)"
    signals:
      VDD: "v(vdd)"
  - label: "Bus Voltages (V)"
    signals:
      Bus01: "v(bus01)"
      Bus02: "v(bus02)"
""")
        
        # Call v1.0.0 plot function
        fig = wv.plot(data, spec, show=False)
        
        # Verify the result
        self.assertIsInstance(fig, go.Figure)
        self.assertEqual(len(fig.data), 3)  # 3 traces
        
        # Check traces
        self.assertEqual(fig.data[0].name, "VDD")
        self.assertEqual(fig.data[1].name, "Bus01")
        self.assertEqual(fig.data[2].name, "Bus02")
        
        # Check Y-axis assignments
        self.assertEqual(fig.data[0].yaxis, "y")    # First Y-axis
        self.assertEqual(fig.data[1].yaxis, "y2")   # Second Y-axis
        self.assertEqual(fig.data[2].yaxis, "y2")   # Second Y-axis
        
        # Check layout
        self.assertEqual(fig.layout.title.text, "Ring Oscillator - Multi-Axis Test")
        self.assertEqual(fig.layout.xaxis.title.text, "time")
        self.assertEqual(fig.layout.yaxis.title.text, "Supply Voltage (V)")
        self.assertEqual(fig.layout.yaxis2.title.text, "Bus Voltages (V)")
        
        print("✅ v1.0.0 plot() function working correctly with multi-axis")

    def test_v1_0_0_plot_with_dict_config(self):
        """Test v1.0.0 plot function with dictionary configuration."""
        # Load real SPICE data
        data, _ = wv.load_spice_raw(self.test_raw_file)
        
        # Create configuration dictionary
        config = {
            "title": "Ring Oscillator - Dict Config Test",
            "x": "time",
            "y": [{
                "label": "Voltages (V)",
                "signals": {
                    "VDD": "v(vdd)",
                    "Bus01": "v(bus01)"
                }
            }]
        }
        
        # Call v1.0.0 plot function
        fig = wv.plot(data, config, show=False)
        
        # Verify the result
        self.assertIsInstance(fig, go.Figure)
        self.assertEqual(len(fig.data), 2)  # 2 traces
        
        # Check traces
        self.assertEqual(fig.data[0].name, "VDD")
        self.assertEqual(fig.data[1].name, "Bus01")
        
        # Check layout
        self.assertEqual(fig.layout.title.text, "Ring Oscillator - Dict Config Test")
        
        print("✅ v1.0.0 plot() function working correctly with dictionary config")


if __name__ == '__main__':
    unittest.main() 