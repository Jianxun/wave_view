"""
Test complex number handling in SPICE AC analysis data.

This module tests that complex numbers from AC analysis are properly preserved
and can be used for transfer function analysis (magnitude and phase calculations).
"""

import unittest
import numpy as np
from unittest.mock import Mock, patch
from pathlib import Path
import os

from wave_view.core.reader import SpiceData


class TestComplexNumberHandling(unittest.TestCase):
    """Test complex number preservation in AC analysis data."""
    
    def setUp(self):
        """Set up test fixtures for complex number testing."""
        # Create mock complex AC data (typical for AC analysis)
        self.complex_ac_data = np.array([
            1.0 + 0.1j,      # DC point with small phase
            0.9 + 0.2j,      # Mid frequency
            0.5 + 0.5j,      # Higher frequency, more phase shift
            0.1 + 0.8j,      # Even higher frequency
            0.01 + 0.99j,    # Near unity phase shift
        ], dtype=np.complex128)
        
        # Create mock frequency data (always real)
        self.frequency_data = np.array([
            1e3, 1e4, 1e5, 1e6, 1e7
        ], dtype=np.float64)
    
    def create_mock_ac_rawread(self):
        """Create mock RawRead for AC analysis with complex data."""
        mock_raw = Mock()
        
        # AC analysis typically has frequency and complex voltage/current signals
        mock_raw.get_trace_names.return_value = [
            "frequency", "v(out)", "v(in)", "i(vdd)"
        ]
        
        def get_trace_side_effect(name):
            if name == "frequency":
                return self.frequency_data
            elif name == "v(out)":
                return self.complex_ac_data
            elif name == "v(in)":
                return np.ones(5, dtype=np.complex128)  # Reference signal
            elif name == "i(vdd)":
                return self.complex_ac_data * 0.1  # Scaled current
            return None
        
        mock_raw.get_trace.side_effect = get_trace_side_effect
        return mock_raw
    
    @patch('wave_view.core.reader.RawRead')
    def test_complex_signals_preserved(self, mock_rawread_class):
        """Test that complex signals from AC analysis are preserved."""
        mock_rawread_class.return_value = self.create_mock_ac_rawread()
        
        spice_data = SpiceData("test_ac.raw")
        
        # Get complex signal
        v_out = spice_data.get_signal("v(out)")
        
        # Verify it's complex
        self.assertTrue(np.iscomplexobj(v_out))
        self.assertEqual(v_out.dtype, np.complex128)
        
        # Verify values are preserved correctly
        np.testing.assert_array_equal(v_out, self.complex_ac_data)
        
        # Verify complex properties
        self.assertFalse(np.all(np.isreal(v_out)))  # Should have imaginary parts
        self.assertTrue(np.all(np.isfinite(v_out)))  # Should be finite
    
    @patch('wave_view.core.reader.RawRead')
    def test_frequency_remains_real(self, mock_rawread_class):
        """Test that frequency data remains real even in AC analysis."""
        mock_rawread_class.return_value = self.create_mock_ac_rawread()
        
        spice_data = SpiceData("test_ac.raw")
        
        # Get frequency signal
        frequency = spice_data.get_signal("frequency")
        
        # Frequency should be real
        self.assertTrue(np.isrealobj(frequency))
        self.assertTrue(np.all(np.isreal(frequency)))
        
        # Verify values
        np.testing.assert_array_equal(frequency, self.frequency_data)
    
    @patch('wave_view.core.reader.RawRead')
    def test_magnitude_phase_calculations(self, mock_rawread_class):
        """Test that magnitude and phase can be calculated from complex data."""
        mock_rawread_class.return_value = self.create_mock_ac_rawread()
        
        spice_data = SpiceData("test_ac.raw")
        v_out = spice_data.get_signal("v(out)")
        
        # Calculate magnitude in dB
        magnitude_db = 20 * np.log10(np.abs(v_out))
        
        # Calculate phase in degrees
        phase_deg = np.angle(v_out) * 180 / np.pi
        
        # Verify calculations work and produce reasonable results
        self.assertTrue(np.all(np.isfinite(magnitude_db)))
        self.assertTrue(np.all(np.isfinite(phase_deg)))
        
        # Check that calculations are valid (no NaN or inf)
        self.assertTrue(np.all(np.isfinite(magnitude_db)))
        self.assertTrue(np.all(np.isfinite(phase_deg)))
        
        # Verify magnitude decreases with frequency (typical low-pass behavior)
        self.assertGreater(magnitude_db[0], magnitude_db[-1])
        
        # Verify phase increases with frequency (typical low-pass behavior)
        self.assertLess(phase_deg[0], phase_deg[-1])
    
    @patch('wave_view.core.reader.RawRead')
    def test_mixed_real_complex_signals(self, mock_rawread_class):
        """Test handling of mixed real and complex signals in same file."""
        mock_rawread_class.return_value = self.create_mock_ac_rawread()
        
        spice_data = SpiceData("test_ac.raw")
        
        # Get mixed signals
        frequency = spice_data.get_signal("frequency")  # Should be real
        v_out = spice_data.get_signal("v(out)")         # Should be complex
        
        # Verify types
        self.assertTrue(np.isrealobj(frequency))
        self.assertTrue(np.iscomplexobj(v_out))
        
        # Both should have same length
        self.assertEqual(len(frequency), len(v_out))
        
        # Get multiple signals at once
        signals = spice_data.get_signals(["frequency", "v(out)", "v(in)"])
        
        # Verify mixed types in result
        self.assertTrue(np.isrealobj(signals["frequency"]))
        self.assertTrue(np.iscomplexobj(signals["v(out)"]))
        self.assertTrue(np.iscomplexobj(signals["v(in)"]))
    
    @patch('wave_view.core.reader.RawRead')
    def test_complex_data_consistency(self, mock_rawread_class):
        """Test that complex data access is consistent across multiple calls."""
        mock_rawread_class.return_value = self.create_mock_ac_rawread()
        
        spice_data = SpiceData("test_ac.raw")
        
        # Get same signal multiple times
        v_out1 = spice_data.get_signal("v(out)")
        v_out2 = spice_data.get_signal("V(OUT)")  # Different case
        v_out3 = spice_data.get_signal("v(out)")  # Same as first
        
        # All should be identical
        np.testing.assert_array_equal(v_out1, v_out2)
        np.testing.assert_array_equal(v_out1, v_out3)
        
        # All should be complex
        self.assertTrue(np.iscomplexobj(v_out1))
        self.assertTrue(np.iscomplexobj(v_out2))
        self.assertTrue(np.iscomplexobj(v_out3))


class TestTransferFunctionWorkflow(unittest.TestCase):
    """Test complete transfer function analysis workflow with complex data."""
    
    @patch('wave_view.core.reader.RawRead')
    def test_bode_plot_data_preparation(self, mock_rawread_class):
        """Test preparing data for Bode plot from AC analysis."""
        # Create realistic AC analysis data
        frequencies = np.logspace(3, 7, 50)  # 1kHz to 10MHz
        
        # Create transfer function: first-order low-pass filter
        # H(s) = 1 / (1 + s*RC) where RC = 1/(2*pi*10kHz)
        fc = 10e3  # 10kHz cutoff
        s = 2j * np.pi * frequencies
        transfer_function = 1 / (1 + s / (2 * np.pi * fc))
        
        mock_raw = Mock()
        mock_raw.get_trace_names.return_value = ["frequency", "v(out)", "v(in)"]
        
        def get_trace_side_effect(name):
            if name == "frequency":
                return frequencies
            elif name == "v(out)":
                return transfer_function  # Complex transfer function
            elif name == "v(in)":
                return np.ones(len(frequencies), dtype=np.complex128)  # Unity input
            return None
        
        mock_raw.get_trace.side_effect = get_trace_side_effect
        mock_rawread_class.return_value = mock_raw
        
        # Load data
        spice_data = SpiceData("test_ac.raw")
        
        # Get signals
        freq = spice_data.get_signal("frequency")
        v_out = spice_data.get_signal("v(out)")
        
        # Prepare Bode plot data
        magnitude_db = 20 * np.log10(np.abs(v_out))
        phase_deg = np.angle(v_out) * 180 / np.pi
        
        # Verify Bode plot data is reasonable
        # Magnitude should decrease with frequency (low-pass behavior)
        self.assertGreater(magnitude_db[0], magnitude_db[-1])
        
        # Phase should change significantly across frequency range
        phase_range = np.max(phase_deg) - np.min(phase_deg)
        self.assertGreater(abs(phase_range), 30)  # At least 30° phase change
        
        # Verify data is finite and reasonable
        self.assertTrue(np.all(np.isfinite(magnitude_db)))
        self.assertTrue(np.all(np.isfinite(phase_deg)))
        self.assertGreater(len(magnitude_db), 10)  # Enough data points


if __name__ == '__main__':
    unittest.main() 