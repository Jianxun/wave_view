import unittest
import numpy as np
import yaml2plot as y2p
from pathlib import Path
import plotly.graph_objects as go  # type: ignore
from typing import Any


class TestSignalProcessingWorkflow(unittest.TestCase):
    """User story: load xarray Dataset, add derived signals, and plot."""

    def test_ac_analysis_signal_processing(self):
        """Test AC analysis with magnitude and phase derived signals using clean xarray API."""
        # Use the actual AC analysis test file (complex signals)
        raw_file = Path("tests/raw_files/ota_ac_results.raw")
        self.assertTrue(raw_file.exists(), f"Missing fixture {raw_file}")
        
        # Load raw data as xarray Dataset
        dataset = y2p.load_spice_raw(raw_file)
        
        # Verify we have AC analysis data with complex signals
        test_signal = "v(out)"  # Use the output signal from OTA AC analysis
        self.assertIn(test_signal, dataset.data_vars)
        
        # Verify this is AC analysis (should have frequency coordinate)
        self.assertIn("frequency", dataset.coords)
        
        # Add derived signals directly to the xarray Dataset using clean API
        # Real AC analysis transfer function magnitude and phase calculations
        signal_data = dataset[test_signal]
        
        # Add transfer function magnitude in dB (|H(jw)| in dB)  
        dataset["tf_db"] = 20*np.log10(np.abs(signal_data))
        
        # Add transfer function phase in degrees (∠H(jw))
        phase_values = np.angle(signal_data) * 180/np.pi
        dataset["tf_phase"] = (signal_data.dims, phase_values)
        
        # Verify derived signals were added correctly
        self.assertIn("tf_db", dataset.data_vars)
        self.assertIn("tf_phase", dataset.data_vars)
        
        # Verify dimensions are preserved automatically
        original_dims = dataset[test_signal].dims
        self.assertEqual(dataset["tf_db"].dims, original_dims)
        self.assertEqual(dataset["tf_phase"].dims, original_dims)
        
        # Test plotting with derived signals
        spec = y2p.PlotSpec.from_yaml("""
        title: "AC Analysis - Transfer Function"
        x:
          signal: "frequency"
          label: "Frequency (Hz)"
          scale: "log"
        y:
          - label: "Magnitude (dB)"
            signals:
              Magnitude: "tf_db"
          - label: "Phase (deg)"
            signals:
              Phase: "tf_phase"
        """)
        
        # Create plot using clean xarray API
        fig = y2p.plot(dataset, spec, show=False)
        
        # Verify plot was created successfully
        self.assertIsInstance(fig, go.Figure)
        
        # Type check the figure data for lint compatibility
        fig_data: Any = fig.data  # Suppress Pylance false positive
        self.assertEqual(len(fig_data), 2)  # Two traces for magnitude and phase
        
        # Verify trace names
        trace_names = [trace.name for trace in fig_data]  # type: ignore
        self.assertIn("Magnitude", trace_names)
        self.assertIn("Phase", trace_names)
        
        # Verify plot has correct structure for dual-axis
        layout = fig.layout
        self.assertEqual(layout.title.text, "AC Analysis - Transfer Function")
        self.assertEqual(layout.xaxis.title.text, "Frequency (Hz)")
        
    def test_frequency_domain_processing(self):
        """Test frequency domain signal processing with xarray Dataset."""
        raw_file = Path("tests/raw_files/Ring_Oscillator_7stage.raw")
        dataset = y2p.load_spice_raw(raw_file)
        
        # Simulate frequency domain processing
        time_signal = "v(bus07)"
        
        # Add power calculation (V²) 
        dataset["power"] = dataset[time_signal] ** 2
        
        # Add normalized signal
        signal_data = dataset[time_signal]
        signal_max = np.max(np.abs(signal_data))
        dataset["normalized"] = signal_data / signal_max
        
        # Verify derived signals
        self.assertIn("power", dataset.data_vars)
        self.assertIn("normalized", dataset.data_vars)
        
        # Test that we can plot multiple derived signals
        spec = y2p.PlotSpec.from_yaml("""
        title: "Multi-signal Processing Test"
        x:
          signal: "time"
        y:
          - label: "Signals"
            signals:
              Original: "v(bus07)"
              Power: "power"
              Normalized: "normalized"
        """)
        
        fig = y2p.plot(dataset, spec, show=False)
        self.assertIsInstance(fig, go.Figure)
        
        # Type check the figure data for lint compatibility
        fig_data: Any = fig.data  # Suppress Pylance false positive
        self.assertEqual(len(fig_data), 3)  # Three traces


if __name__ == "__main__":
    unittest.main()