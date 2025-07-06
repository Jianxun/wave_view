"""
Integration test for v1.0.0 API with real SPICE data.

This test verifies that the new v1.0.0 plotting functions work correctly
with real SPICE data files.
"""

import unittest
import numpy as np
import wave_view as wv
from pathlib import Path


class TestV1_0_0Integration(unittest.TestCase):
    """Integration test for v1.0.0 API."""
    
    def setUp(self):
        """Set up test with real SPICE data."""
        # Use the existing test raw file
        self.test_raw_file = Path("tests/raw_files/Ring_Oscillator_7stage.raw")
        
        # Skip if test file doesn't exist
        if not self.test_raw_file.exists():
            self.skipTest(f"Test SPICE file not found: {self.test_raw_file}")
    
    def test_v1_0_0_plot_with_real_data(self):
        """Test v1.0.0 plot function with real SPICE data."""
        # Load real SPICE data
        spice_data = wv.load_spice(self.test_raw_file)
        
        # Convert to v1.0.0 format (Dict[str, np.ndarray])
        data = {}
        for signal_name in spice_data.signals:
            data[signal_name] = spice_data.get_signal(signal_name)
        
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
        fig = wv.plot_v1(data, spec)
        
        # Verify the figure was created successfully
        self.assertIsNotNone(fig)
        
        # Verify it has the expected structure
        self.assertEqual(len(fig.data), 2)  # Two traces
        trace_names = [trace.name for trace in fig.data]
        self.assertIn("VDD", trace_names)
        self.assertIn("Bus01", trace_names)
        self.assertEqual(fig.layout.title.text, "Ring Oscillator - v1.0.0 Test")
        
        # Verify data is correct
        vdd_trace = next(trace for trace in fig.data if trace.name == "VDD")
        bus01_trace = next(trace for trace in fig.data if trace.name == "Bus01")
        
        self.assertEqual(len(vdd_trace.x), len(data["time"]))
        self.assertEqual(len(vdd_trace.y), len(data["v(vdd)"]))
        np.testing.assert_array_equal(vdd_trace.x, data["time"])
        np.testing.assert_array_equal(vdd_trace.y, data["v(vdd)"])
        
        self.assertEqual(len(bus01_trace.x), len(data["time"]))
        self.assertEqual(len(bus01_trace.y), len(data["v(bus01)"]))
        np.testing.assert_array_equal(bus01_trace.x, data["time"])
        np.testing.assert_array_equal(bus01_trace.y, data["v(bus01)"])
    
    def test_v1_0_0_plot_with_multi_axis(self):
        """Test v1.0.0 plot function with multi-axis configuration."""
        # Load real SPICE data
        spice_data = wv.load_spice(self.test_raw_file)
        
        # Convert to v1.0.0 format
        data = {}
        for signal_name in spice_data.signals:
            data[signal_name] = spice_data.get_signal(signal_name)
        
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
        fig = wv.plot_v1(data, spec)
        
        # Verify multi-axis structure
        self.assertEqual(len(fig.data), 3)  # Three traces
        
        # Verify Y-axis assignments
        vdd_trace = next(trace for trace in fig.data if trace.name == "VDD")
        bus01_trace = next(trace for trace in fig.data if trace.name == "Bus01")
        bus02_trace = next(trace for trace in fig.data if trace.name == "Bus02")
        
        self.assertEqual(vdd_trace.yaxis, "y")   # First Y-axis
        self.assertEqual(bus01_trace.yaxis, "y2")  # Second Y-axis
        self.assertEqual(bus02_trace.yaxis, "y2")  # Second Y-axis
        
        # Verify layout has two Y-axes
        self.assertIn("yaxis", fig.layout)
        self.assertIn("yaxis2", fig.layout)
        
        # Verify axis titles
        self.assertEqual(fig.layout.yaxis.title.text, "Supply Voltage (V)")
        self.assertEqual(fig.layout.yaxis2.title.text, "Bus Voltages (V)")


if __name__ == '__main__':
    unittest.main() 