"""
Unit tests for SpiceData edge cases and error conditions.

This module tests error handling, edge cases, and unusual scenarios
that may occur with SPICE file reading and signal access.
"""

import unittest
import tempfile
import os
from unittest.mock import patch, Mock
import numpy as np

from wave_view.core.reader import SpiceData
from . import (
    create_temporary_invalid_file, cleanup_temporary_file,
    create_mock_spicelib_rawread, create_mock_empty_rawread,
    assert_signal_data_integrity
)


class TestFileSystemEdgeCases(unittest.TestCase):
    """Test file system related edge cases."""
    
    def test_nonexistent_file(self):
        """Test loading completely nonexistent file."""
        with self.assertRaises(FileNotFoundError) as context:
            SpiceData("/path/to/nonexistent/file.raw")
        
        error_msg = str(context.exception)
        self.assertIn("SPICE raw file not found", error_msg)
        self.assertIn("/path/to/nonexistent/file.raw", error_msg)
    
    @patch('wave_view.core.reader.RawRead')
    def test_invalid_file_format(self, mock_rawread_class):
        """Test loading file with invalid format that spicelib can't read."""
        mock_rawread_class.side_effect = Exception("Binary file format error")
        
        with self.assertRaises(Exception) as context:
            SpiceData("invalid_format.raw")
        
        error_msg = str(context.exception)
        self.assertIn("Failed to read SPICE raw file", error_msg)
        self.assertIn("invalid_format.raw", error_msg)
        self.assertIn("Binary file format error", error_msg)
    
    def test_empty_filename(self):
        """Test loading with empty filename."""
        with self.assertRaises(Exception):  # Could be FileNotFoundError or directory error
            SpiceData("")
    
    @patch('wave_view.core.reader.RawRead')
    def test_permission_error(self, mock_rawread_class):
        """Test handling permission errors."""
        mock_rawread_class.side_effect = PermissionError("Permission denied")
        
        with self.assertRaises(Exception) as context:
            SpiceData("protected_file.raw")
        
        self.assertIn("Failed to read SPICE raw file", str(context.exception))
        self.assertIn("Permission denied", str(context.exception))


class TestSpecialSignalNames(unittest.TestCase):
    """Test handling of special signal name formats."""
    
    @patch('wave_view.core.reader.RawRead')
    def test_signal_names_with_special_characters(self, mock_rawread_class):
        """Test signals with dots, colons, and other special characters."""
        mock_raw = Mock()
        special_signals = [
            "time", "V(net.1)", "I(R1)", "IX(M1:D)", "IX(M1:G)", 
            "V(bus[0])", "V(clk_div)", "I(L1)", "V(n_001)"
        ]
        mock_raw.get_trace_names.return_value = special_signals
        
        def get_trace_side_effect(name):
            if name in special_signals:
                return np.ones(50) * 1.0
            return None
        
        mock_raw.get_trace.side_effect = get_trace_side_effect
        mock_rawread_class.return_value = mock_raw
        
        spice_data = SpiceData("test.raw")
        
        # Check that all signals are accessible (case insensitive)
        for signal in special_signals:
            with self.subTest(signal=signal):
                self.assertTrue(spice_data.has_signal(signal))
                self.assertTrue(spice_data.has_signal(signal.lower()))
                
                # Should be able to get the signal data
                data = spice_data.get_signal(signal)
                assert_signal_data_integrity(data, expected_length=50)
    
    @patch('wave_view.core.reader.RawRead')
    def test_unicode_signal_names(self, mock_rawread_class):
        """Test handling of unicode characters in signal names."""
        mock_raw = Mock()
        unicode_signals = ["time", "V(α)", "I(β_resistor)", "V(δ_node)"]
        mock_raw.get_trace_names.return_value = unicode_signals
        
        def get_trace_side_effect(name):
            if name in unicode_signals:
                return np.ones(30) * 0.5
            return None
        
        mock_raw.get_trace.side_effect = get_trace_side_effect
        mock_rawread_class.return_value = mock_raw
        
        spice_data = SpiceData("unicode.raw")
        
        # Check unicode signals are handled correctly
        for signal in unicode_signals:
            with self.subTest(signal=signal):
                self.assertTrue(spice_data.has_signal(signal))
                data = spice_data.get_signal(signal)
                self.assertEqual(len(data), 30)
    
    @patch('wave_view.core.reader.RawRead')
    def test_very_long_signal_names(self, mock_rawread_class):
        """Test handling of very long signal names."""
        mock_raw = Mock()
        long_signal = "V(" + "very_long_node_name_" * 10 + "end)"  # Very long name
        signals = ["time", long_signal]
        mock_raw.get_trace_names.return_value = signals
        
        def get_trace_side_effect(name):
            if name in signals:
                return np.ones(25) * 2.0
            return None
        
        mock_raw.get_trace.side_effect = get_trace_side_effect
        mock_rawread_class.return_value = mock_raw
        
        spice_data = SpiceData("long_names.raw")
        
        # Should handle long signal names correctly
        self.assertTrue(spice_data.has_signal(long_signal))
        data = spice_data.get_signal(long_signal)
        assert_signal_data_integrity(data, expected_length=25)


class TestDataTypeEdgeCases(unittest.TestCase):
    """Test edge cases related to data types and values."""
    
    @patch('wave_view.core.reader.RawRead')
    def test_zero_length_signals(self, mock_rawread_class):
        """Test handling of zero-length signal data."""
        mock_raw = Mock()
        mock_raw.get_trace_names.return_value = ["time", "V(zero)"]
        
        def get_trace_side_effect(name):
            if name == "time":
                return np.array([])  # Empty time array
            elif name == "V(zero)":
                return np.array([])  # Empty signal array
            return None
        
        mock_raw.get_trace.side_effect = get_trace_side_effect
        mock_rawread_class.return_value = mock_raw
        
        spice_data = SpiceData("zero_length.raw")
        
        # Should handle empty arrays gracefully
        time_data = spice_data.time
        self.assertEqual(len(time_data), 0)
        self.assertIsInstance(time_data, np.ndarray)
        
        signal_data = spice_data.get_signal("V(zero)")
        self.assertEqual(len(signal_data), 0)
        self.assertIsInstance(signal_data, np.ndarray)
    
    @patch('wave_view.core.reader.RawRead')
    def test_signals_with_nan_values(self, mock_rawread_class):
        """Test handling of signals containing NaN values."""
        mock_raw = Mock()
        mock_raw.get_trace_names.return_value = ["time", "V(nan_signal)"]
        
        def get_trace_side_effect(name):
            if name == "time":
                return np.linspace(0, 1e-6, 10)
            elif name == "V(nan_signal)":
                data = np.ones(10)
                data[5] = np.nan  # Insert NaN value
                return data
            return None
        
        mock_raw.get_trace.side_effect = get_trace_side_effect
        mock_rawread_class.return_value = mock_raw
        
        spice_data = SpiceData("nan_values.raw")
        
        # Should return data with NaN values intact
        signal_data = spice_data.get_signal("V(nan_signal)")
        self.assertEqual(len(signal_data), 10)
        self.assertTrue(np.isnan(signal_data[5]))
        self.assertEqual(signal_data.dtype, float)
    
    @patch('wave_view.core.reader.RawRead')
    def test_signals_with_infinite_values(self, mock_rawread_class):
        """Test handling of signals containing infinite values."""
        mock_raw = Mock()
        mock_raw.get_trace_names.return_value = ["time", "V(inf_signal)"]
        
        def get_trace_side_effect(name):
            if name == "time":
                return np.linspace(0, 1e-6, 8)
            elif name == "V(inf_signal)":
                data = np.ones(8)
                data[2] = np.inf
                data[6] = -np.inf
                return data
            return None
        
        mock_raw.get_trace.side_effect = get_trace_side_effect
        mock_rawread_class.return_value = mock_raw
        
        spice_data = SpiceData("inf_values.raw")
        
        # Should handle infinite values
        signal_data = spice_data.get_signal("V(inf_signal)")
        self.assertTrue(np.isinf(signal_data[2]))
        self.assertTrue(np.isinf(signal_data[6]))
        self.assertEqual(signal_data.dtype, float)


class TestErrorMessageQuality(unittest.TestCase):
    """Test quality and helpfulness of error messages."""
    
    @patch('wave_view.core.reader.RawRead')
    def test_signal_not_found_error_message_quality(self, mock_rawread_class):
        """Test that signal not found errors provide helpful information."""
        mock_rawread_class.return_value = create_mock_spicelib_rawread()
        
        spice_data = SpiceData("test.raw")
        
        with self.assertRaises(ValueError) as context:
            spice_data.get_signal("v(definitely_does_not_exist)")
        
        error_msg = str(context.exception)
        
        # Should contain helpful information
        self.assertIn("v(definitely_does_not_exist)", error_msg)
        self.assertIn("not found in raw file", error_msg)
        self.assertIn("Available signals", error_msg)
        
        # Should show some actual signal names
        self.assertIn("time", error_msg)
        self.assertIn("v(vdd)", error_msg)
    
    @patch('wave_view.core.reader.RawRead')
    def test_signal_not_found_with_many_signals(self, mock_rawread_class):
        """Test error message when file has many signals (truncation)."""
        mock_raw = Mock()
        
        # Create a file with many signals (more than 5)
        many_signals = [f"signal_{i:03d}" for i in range(20)]
        mock_raw.get_trace_names.return_value = many_signals
        mock_raw.get_trace.return_value = None
        mock_rawread_class.return_value = mock_raw
        
        spice_data = SpiceData("many_signals.raw")
        
        with self.assertRaises(ValueError) as context:
            spice_data.get_signal("nonexistent")
        
        error_msg = str(context.exception)
        
        # Should truncate signal list and show total count
        self.assertIn("... (20 total)", error_msg)
        self.assertIn("signal_000", error_msg)  # First few signals shown
    
    @patch('wave_view.core.reader.RawRead')
    def test_case_sensitive_signal_suggestion(self, mock_rawread_class):
        """Test error messages with similar signal names (case differences)."""
        mock_raw = Mock()
        mock_raw.get_trace_names.return_value = ["time", "V(VDD)", "V(OUT)"]
        mock_raw.get_trace.return_value = None
        mock_rawread_class.return_value = mock_raw
        
        spice_data = SpiceData("case_test.raw")
        
        # Try to access with wrong case - should fail but provide helpful info
        with self.assertRaises(ValueError) as context:
            spice_data.get_signal("V(WRONG)")
        
        error_msg = str(context.exception)
        self.assertIn("Available signals", error_msg)
        self.assertIn("v(vdd)", error_msg)  # Shows normalized names


class TestConcurrentAccess(unittest.TestCase):
    """Test behavior with concurrent or repeated access patterns."""
    
    @patch('wave_view.core.reader.RawRead')
    def test_repeated_signal_access_consistency(self, mock_rawread_class):
        """Test that repeated signal access returns consistent results."""
        mock_rawread_class.return_value = create_mock_spicelib_rawread()
        
        spice_data = SpiceData("test.raw")
        
        # Access the same signal multiple times
        signal_name = "V(VDD)"
        data1 = spice_data.get_signal(signal_name)
        data2 = spice_data.get_signal(signal_name)
        data3 = spice_data.get_signal(signal_name.lower())
        
        # All should be identical
        np.testing.assert_array_equal(data1, data2)
        np.testing.assert_array_equal(data1, data3)
    
    @patch('wave_view.core.reader.RawRead')
    def test_properties_caching_behavior(self, mock_rawread_class):
        """Test that properties behave consistently on repeated access."""
        mock_rawread_class.return_value = create_mock_spicelib_rawread()
        
        spice_data = SpiceData("test.raw")
        
        # Access properties multiple times
        signals1 = spice_data.signals
        signals2 = spice_data.signals
        
        time1 = spice_data.time
        time2 = spice_data.time
        
        info1 = spice_data.info
        info2 = spice_data.info
        
        # Should return consistent results
        self.assertEqual(signals1, signals2)
        np.testing.assert_array_equal(time1, time2)
        self.assertEqual(info1, info2)


class TestMemoryAndPerformance(unittest.TestCase):
    """Test memory usage and performance edge cases."""
    
    @patch('wave_view.core.reader.RawRead')
    def test_large_signal_count(self, mock_rawread_class):
        """Test handling of files with very large numbers of signals."""
        mock_raw = Mock()
        
        # Simulate a file with 1000 signals
        large_signal_list = [f"signal_{i:04d}" for i in range(1000)]
        mock_raw.get_trace_names.return_value = large_signal_list
        
        def get_trace_side_effect(name):
            if name in large_signal_list:
                return np.ones(10)  # Small arrays to keep test fast
            return None
        
        mock_raw.get_trace.side_effect = get_trace_side_effect
        mock_rawread_class.return_value = mock_raw
        
        spice_data = SpiceData("large_signal_count.raw")
        
        # Should handle large signal lists
        signals = spice_data.signals
        self.assertEqual(len(signals), 1000)
        
        # Should be able to access individual signals
        data = spice_data.get_signal("signal_0500")
        self.assertEqual(len(data), 10)
        
        # Info should report correct count
        info = spice_data.info
        self.assertEqual(info["signal_count"], 1000)


if __name__ == '__main__':
    unittest.main() 