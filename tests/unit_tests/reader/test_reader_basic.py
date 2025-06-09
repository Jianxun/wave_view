"""
Unit tests for SpiceData basic functionality.

This module tests the core SpiceData functionality using mocked spicelib
to ensure consistent behavior without file system dependencies.
"""

import unittest
from unittest.mock import patch, Mock
import numpy as np

from wave_view.core.reader import SpiceData
from . import (
    create_mock_spicelib_rawread, create_mock_empty_rawread, 
    create_mock_no_time_rawread, assert_signal_data_integrity,
    assert_signal_list_format, assert_spice_data_info_structure,
    get_test_signal_variations
)


class TestSpiceDataInitialization(unittest.TestCase):
    """Test SpiceData initialization and basic setup."""
    
    @patch('wave_view.core.reader.RawRead')
    def test_successful_initialization(self, mock_rawread_class):
        """Test successful initialization with valid file."""
        mock_rawread_class.return_value = create_mock_spicelib_rawread()
        
        spice_data = SpiceData("test.raw")
        
        # Check initialization
        self.assertIsNotNone(spice_data)
        self.assertEqual(spice_data._raw_file_path, "test.raw")
        mock_rawread_class.assert_called_once_with("test.raw")
    
    @patch('wave_view.core.reader.RawRead')
    def test_file_not_found_error(self, mock_rawread_class):
        """Test FileNotFoundError handling."""
        mock_rawread_class.side_effect = FileNotFoundError("File not found")
        
        with self.assertRaises(FileNotFoundError) as context:
            SpiceData("nonexistent.raw")
        
        self.assertIn("SPICE raw file not found", str(context.exception))
        self.assertIn("nonexistent.raw", str(context.exception))
    
    @patch('wave_view.core.reader.RawRead')
    def test_generic_read_error(self, mock_rawread_class):
        """Test generic read error handling."""
        mock_rawread_class.side_effect = RuntimeError("Invalid file format")
        
        with self.assertRaises(Exception) as context:
            SpiceData("invalid.raw")
        
        self.assertIn("Failed to read SPICE raw file", str(context.exception))
        self.assertIn("invalid.raw", str(context.exception))
        self.assertIn("Invalid file format", str(context.exception))


class TestSignalsProperty(unittest.TestCase):
    """Test the signals property functionality."""
    
    @patch('wave_view.core.reader.RawRead')
    def test_signals_property_basic(self, mock_rawread_class):
        """Test basic signals property functionality."""
        mock_rawread_class.return_value = create_mock_spicelib_rawread()
        
        spice_data = SpiceData("test.raw")
        signals = spice_data.signals
        
        # Check signal list format and content
        assert_signal_list_format(signals)
        expected_signals = ["time", "v(vdd)", "v(out)", "i(vdd)", "v(bus01)", "i(c1)"]
        self.assertEqual(signals, expected_signals)
    
    @patch('wave_view.core.reader.RawRead')
    def test_signals_property_case_normalization(self, mock_rawread_class):
        """Test that signals are normalized to lowercase."""
        mock_raw = Mock()
        mock_raw.get_trace_names.return_value = ["TIME", "V(VDD)", "V(Out)", "I(VDD)"]
        mock_rawread_class.return_value = mock_raw
        
        spice_data = SpiceData("test.raw")
        signals = spice_data.signals
        
        expected_lowercase = ["time", "v(vdd)", "v(out)", "i(vdd)"]
        self.assertEqual(signals, expected_lowercase)
    
    @patch('wave_view.core.reader.RawRead')
    def test_signals_property_empty_file(self, mock_rawread_class):
        """Test signals property with empty file."""
        mock_rawread_class.return_value = create_mock_empty_rawread()
        
        spice_data = SpiceData("empty.raw")
        signals = spice_data.signals
        
        self.assertEqual(signals, [])
        self.assertIsInstance(signals, list)


class TestTimeProperty(unittest.TestCase):
    """Test the time property functionality."""
    
    @patch('wave_view.core.reader.RawRead')
    def test_time_property_basic(self, mock_rawread_class):
        """Test basic time property functionality."""
        mock_rawread_class.return_value = create_mock_spicelib_rawread()
        
        spice_data = SpiceData("test.raw")
        time_data = spice_data.time
        
        # Validate time data
        assert_signal_data_integrity(time_data, expected_length=100)
        
        # Check time is monotonic
        self.assertTrue(np.all(np.diff(time_data) > 0))
        
        # Check time range
        self.assertAlmostEqual(time_data[0], 0.0, places=10)
        self.assertAlmostEqual(time_data[-1], 1e-6, places=10)
    
    @patch('wave_view.core.reader.RawRead')
    def test_time_property_not_available(self, mock_rawread_class):
        """Test time property when time data is not available."""
        mock_rawread_class.return_value = create_mock_no_time_rawread()
        
        spice_data = SpiceData("test.raw")
        
        with self.assertRaises(ValueError) as context:
            _ = spice_data.time
        
        self.assertIn("Time data not found", str(context.exception))


class TestInfoProperty(unittest.TestCase):
    """Test the info property functionality."""
    
    @patch('wave_view.core.reader.RawRead')
    def test_info_property_structure(self, mock_rawread_class):
        """Test info property returns correct structure."""
        mock_rawread_class.return_value = create_mock_spicelib_rawread()
        
        spice_data = SpiceData("test.raw")
        info = spice_data.info
        
        assert_spice_data_info_structure(info, expected_file_path="test.raw")
        
        # Check specific content
        self.assertEqual(info["signal_count"], 6)  # Mock has 6 signals
        self.assertEqual(len(info["signals"]), 6)
        
        # Check signals are included
        expected_signals = ["time", "v(vdd)", "v(out)", "i(vdd)", "v(bus01)", "i(c1)"]
        self.assertEqual(info["signals"], expected_signals)
    
    @patch('wave_view.core.reader.RawRead')
    def test_info_property_empty_file(self, mock_rawread_class):
        """Test info property with empty file."""
        mock_rawread_class.return_value = create_mock_empty_rawread()
        
        spice_data = SpiceData("empty.raw")
        info = spice_data.info
        
        assert_spice_data_info_structure(info, expected_file_path="empty.raw")
        self.assertEqual(info["signal_count"], 0)
        self.assertEqual(info["signals"], [])


class TestGetSignalMethod(unittest.TestCase):
    """Test the get_signal method functionality."""
    
    @patch('wave_view.core.reader.RawRead')
    def test_get_signal_basic(self, mock_rawread_class):
        """Test basic get_signal functionality."""
        mock_rawread_class.return_value = create_mock_spicelib_rawread()
        
        spice_data = SpiceData("test.raw")
        
        # Test getting VDD signal
        vdd_data = spice_data.get_signal("V(VDD)")
        assert_signal_data_integrity(vdd_data, expected_length=100)
        self.assertTrue(np.allclose(vdd_data, 1.8))  # Mock VDD is 1.8V
    
    @patch('wave_view.core.reader.RawRead')
    def test_get_signal_case_insensitive(self, mock_rawread_class):
        """Test case insensitive signal access."""
        mock_rawread_class.return_value = create_mock_spicelib_rawread()
        
        spice_data = SpiceData("test.raw")
        
        # Test various case combinations
        variations = get_test_signal_variations("V(VDD)")
        base_data = spice_data.get_signal("V(VDD)")
        
        for variation in variations:
            with self.subTest(variation=variation):
                data = spice_data.get_signal(variation)
                np.testing.assert_array_equal(data, base_data)
    
    @patch('wave_view.core.reader.RawRead')
    def test_get_signal_not_found(self, mock_rawread_class):
        """Test get_signal with non-existent signal."""
        mock_rawread_class.return_value = create_mock_spicelib_rawread()
        
        spice_data = SpiceData("test.raw")
        
        with self.assertRaises(ValueError) as context:
            spice_data.get_signal("v(nonexistent)")
        
        error_msg = str(context.exception)
        self.assertIn("not found in raw file", error_msg)
        self.assertIn("Available signals", error_msg)
        self.assertIn("time", error_msg)  # Should show available signals
    
    @patch('wave_view.core.reader.RawRead')
    def test_get_signal_data_types(self, mock_rawread_class):
        """Test that get_signal returns proper data types."""
        mock_rawread_class.return_value = create_mock_spicelib_rawread()
        
        spice_data = SpiceData("test.raw")
        
        signals_to_test = ["time", "V(VDD)", "V(OUT)", "I(VDD)"]
        for signal in signals_to_test:
            with self.subTest(signal=signal):
                data = spice_data.get_signal(signal)
                self.assertIsInstance(data, np.ndarray)
                self.assertEqual(data.dtype, float)


class TestHasSignalMethod(unittest.TestCase):
    """Test the has_signal method functionality."""
    
    @patch('wave_view.core.reader.RawRead')
    def test_has_signal_existing(self, mock_rawread_class):
        """Test has_signal with existing signals."""
        mock_rawread_class.return_value = create_mock_spicelib_rawread()
        
        spice_data = SpiceData("test.raw")
        
        existing_signals = ["time", "V(VDD)", "v(vdd)", "V(OUT)", "I(VDD)"]
        for signal in existing_signals:
            with self.subTest(signal=signal):
                self.assertTrue(spice_data.has_signal(signal))
    
    @patch('wave_view.core.reader.RawRead')
    def test_has_signal_nonexisting(self, mock_rawread_class):
        """Test has_signal with non-existent signals."""
        mock_rawread_class.return_value = create_mock_spicelib_rawread()
        
        spice_data = SpiceData("test.raw")
        
        nonexisting_signals = ["v(fake)", "i(missing)", "random_signal", ""]
        for signal in nonexisting_signals:
            with self.subTest(signal=signal):
                self.assertFalse(spice_data.has_signal(signal))
    
    @patch('wave_view.core.reader.RawRead')
    def test_has_signal_case_insensitive(self, mock_rawread_class):
        """Test has_signal is case insensitive."""
        mock_rawread_class.return_value = create_mock_spicelib_rawread()
        
        spice_data = SpiceData("test.raw")
        
        variations = get_test_signal_variations("V(VDD)")
        for variation in variations:
            with self.subTest(variation=variation):
                self.assertTrue(spice_data.has_signal(variation))


class TestGetSignalsMethod(unittest.TestCase):
    """Test the get_signals method functionality."""
    
    @patch('wave_view.core.reader.RawRead')
    def test_get_signals_basic(self, mock_rawread_class):
        """Test basic get_signals functionality."""
        mock_rawread_class.return_value = create_mock_spicelib_rawread()
        
        spice_data = SpiceData("test.raw")
        
        signal_names = ["V(VDD)", "I(VDD)", "time"]
        result = spice_data.get_signals(signal_names)
        
        # Check result structure
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 3)
        
        # Check normalized keys
        expected_keys = ["v(vdd)", "i(vdd)", "time"]
        for key in expected_keys:
            self.assertIn(key, result)
            assert_signal_data_integrity(result[key], expected_length=100)
    
    @patch('wave_view.core.reader.RawRead')
    def test_get_signals_empty_list(self, mock_rawread_class):
        """Test get_signals with empty signal list."""
        mock_rawread_class.return_value = create_mock_spicelib_rawread()
        
        spice_data = SpiceData("test.raw")
        result = spice_data.get_signals([])
        
        self.assertEqual(result, {})
        self.assertIsInstance(result, dict)
    
    @patch('wave_view.core.reader.RawRead')
    def test_get_signals_with_invalid(self, mock_rawread_class):
        """Test get_signals with invalid signal in list."""
        mock_rawread_class.return_value = create_mock_spicelib_rawread()
        
        spice_data = SpiceData("test.raw")
        
        signal_names = ["V(VDD)", "v(invalid)", "time"]
        
        with self.assertRaises(ValueError) as context:
            spice_data.get_signals(signal_names)
        
        self.assertIn("v(invalid)", str(context.exception))


class TestStringRepresentation(unittest.TestCase):
    """Test string representation functionality."""
    
    @patch('wave_view.core.reader.RawRead')
    def test_repr_basic(self, mock_rawread_class):
        """Test __repr__ method."""
        mock_rawread_class.return_value = create_mock_spicelib_rawread()
        
        spice_data = SpiceData("test_file.raw")
        repr_str = repr(spice_data)
        
        self.assertIn("SpiceData", repr_str)
        self.assertIn("test_file.raw", repr_str)
        self.assertIn("6 signals", repr_str)  # Mock has 6 signals
    
    @patch('wave_view.core.reader.RawRead')
    def test_repr_empty_file(self, mock_rawread_class):
        """Test __repr__ method with empty file."""
        mock_rawread_class.return_value = create_mock_empty_rawread()
        
        spice_data = SpiceData("empty.raw")
        repr_str = repr(spice_data)
        
        self.assertIn("SpiceData", repr_str)
        self.assertIn("empty.raw", repr_str)
        self.assertIn("0 signals", repr_str)


if __name__ == '__main__':
    unittest.main() 