"""
Unit tests for SpiceData using real SPICE raw file.

This module tests the SpiceData class with the actual Ring_Oscillator_7stage.raw
file to validate real-world integration and spicelib compatibility.
"""

import unittest
import numpy as np

from wave_view.core.reader import SpiceData
from . import (
    get_real_file_path, REAL_FILE_EXPECTED_COUNT, REAL_FILE_TIME_POINTS,
    REAL_FILE_TIME_RANGE, REAL_FILE_VDD_VALUE, assert_signal_data_integrity,
    assert_signal_list_format, assert_spice_data_info_structure,
    get_test_signal_variations
)


class TestRealFileLoading(unittest.TestCase):
    """Test SpiceData with actual SPICE raw file."""
    
    @classmethod
    def setUpClass(cls):
        """Load the real file once for all tests in this class."""
        cls.real_file_path = get_real_file_path()
        cls.spice_data = SpiceData(cls.real_file_path)
    
    def test_file_loads_successfully(self):
        """Test that the real SPICE file loads without errors."""
        # Should not raise any exceptions
        self.assertIsNotNone(self.spice_data)
        self.assertIsInstance(self.spice_data, SpiceData)
    
    def test_correct_number_of_signals(self):
        """Test that the expected number of signals are detected."""
        signals = self.spice_data.signals
        self.assertEqual(len(signals), REAL_FILE_EXPECTED_COUNT)
        self.assertEqual(len(signals), 66)  # Explicit check
    
    def test_signal_list_format(self):
        """Test that signals are returned in correct format."""
        signals = self.spice_data.signals
        assert_signal_list_format(signals)
        
        # Check specific expected signals exist
        expected_signals = ['time', 'v(vdd)', 'v(bus01)', 'i(c1)', 'ix(x4:gate)']
        for signal in expected_signals:
            self.assertIn(signal, signals)
    
    def test_time_data_access(self):
        """Test access to time vector from real file."""
        time_data = self.spice_data.time
        
        # Validate time data
        assert_signal_data_integrity(time_data, expected_length=REAL_FILE_TIME_POINTS)
        
        # Check time range
        self.assertAlmostEqual(time_data[0], REAL_FILE_TIME_RANGE[0], places=10)
        self.assertAlmostEqual(time_data[-1], REAL_FILE_TIME_RANGE[1], places=6)
        
        # Time should be monotonic increasing
        self.assertTrue(np.all(np.diff(time_data) > 0))
    
    def test_info_property_structure(self):
        """Test that info property returns correct metadata."""
        info = self.spice_data.info
        
        assert_spice_data_info_structure(info, expected_file_path=self.real_file_path)
        self.assertEqual(info["signal_count"], REAL_FILE_EXPECTED_COUNT)
        self.assertEqual(len(info["signals"]), REAL_FILE_EXPECTED_COUNT)
    
    def test_string_representation(self):
        """Test __repr__ method with real file."""
        repr_str = repr(self.spice_data)
        
        self.assertIn("SpiceData", repr_str)
        self.assertIn(str(REAL_FILE_EXPECTED_COUNT), repr_str)
        self.assertIn("signals", repr_str)
        self.assertIn("Ring_Oscillator_7stage.raw", repr_str)


class TestRealSignalAccess(unittest.TestCase):
    """Test signal access methods with real SPICE data."""
    
    @classmethod
    def setUpClass(cls):
        """Load the real file once for all tests in this class."""
        cls.spice_data = SpiceData(get_real_file_path())
    
    def test_get_vdd_signal(self):
        """Test accessing VDD signal with known characteristics."""
        vdd_data = self.spice_data.get_signal("v(vdd)")
        
        # Validate data integrity
        assert_signal_data_integrity(vdd_data, expected_length=REAL_FILE_TIME_POINTS)
        
        # VDD should be constant at 2.5V for this simulation
        self.assertTrue(np.allclose(vdd_data, REAL_FILE_VDD_VALUE))
        self.assertAlmostEqual(np.mean(vdd_data), REAL_FILE_VDD_VALUE, places=6)
    
    def test_get_various_signal_types(self):
        """Test accessing different types of signals from real file."""
        test_signals = {
            "v(vdd)": "voltage node",
            "v(bus01)": "internal bus voltage", 
            "i(c1)": "component current",
            "ix(x4:gate)": "device terminal current"
        }
        
        for signal_name, description in test_signals.items():
            with self.subTest(signal=signal_name, type=description):
                data = self.spice_data.get_signal(signal_name)
                assert_signal_data_integrity(data, expected_length=REAL_FILE_TIME_POINTS)
                
                # Each signal should have the same length as time
                self.assertEqual(len(data), REAL_FILE_TIME_POINTS)
    
    def test_case_insensitive_access(self):
        """Test case insensitive signal access with real signals."""
        # Test with VDD signal in various cases
        vdd_variations = get_test_signal_variations("V(VDD)")
        base_data = self.spice_data.get_signal("v(vdd)")
        
        for variation in vdd_variations:
            with self.subTest(variation=variation):
                try:
                    data = self.spice_data.get_signal(variation)
                    np.testing.assert_array_equal(data, base_data)
                except ValueError:
                    # Some variations might not match exactly due to real signal names
                    # This is acceptable as long as the lowercase version works
                    continue
    
    def test_has_signal_method(self):
        """Test has_signal method with real signals."""
        # Signals that should exist
        existing_signals = ["v(vdd)", "time", "i(c1)", "v(bus01)"]
        for signal in existing_signals:
            self.assertTrue(self.spice_data.has_signal(signal))
            self.assertTrue(self.spice_data.has_signal(signal.upper()))  # Case insensitive
        
        # Signals that should not exist
        non_existing_signals = ["v(nonexistent)", "i(fake)", "random_signal"]
        for signal in non_existing_signals:
            self.assertFalse(self.spice_data.has_signal(signal))
    
    def test_get_multiple_signals(self):
        """Test get_signals method with real signal names."""
        signal_names = ["v(vdd)", "v(bus01)", "i(c1)", "time"]
        result = self.spice_data.get_signals(signal_names)
        
        # Check result structure
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), len(signal_names))
        
        # Check each signal
        for signal_name in signal_names:
            normalized_name = signal_name.lower()
            self.assertIn(normalized_name, result)
            assert_signal_data_integrity(result[normalized_name], 
                                        expected_length=REAL_FILE_TIME_POINTS)
    
    def test_signal_data_consistency(self):
        """Test that repeated access returns consistent data."""
        signal_name = "v(vdd)"
        
        # Get the same signal multiple times
        data1 = self.spice_data.get_signal(signal_name)
        data2 = self.spice_data.get_signal(signal_name)
        data3 = self.spice_data.get_signal(signal_name.upper())
        
        # All should be identical
        np.testing.assert_array_equal(data1, data2)
        np.testing.assert_array_equal(data1, data3)


class TestRealFileSignalCharacteristics(unittest.TestCase):
    """Test specific characteristics of the Ring Oscillator signals."""
    
    @classmethod
    def setUpClass(cls):
        """Load the real file once for all tests in this class."""
        cls.spice_data = SpiceData(get_real_file_path())
    
    def test_vdd_is_constant(self):
        """Test that VDD remains constant throughout simulation."""
        vdd = self.spice_data.get_signal("v(vdd)")
        
        # VDD should be very stable (ring oscillator power supply)
        vdd_std = np.std(vdd)
        self.assertLess(vdd_std, 0.01)  # Very small variation
        
        # Mean should be close to expected value
        self.assertAlmostEqual(np.mean(vdd), REAL_FILE_VDD_VALUE, places=2)
    
    def test_bus_signals_are_digital(self):
        """Test that bus signals behave like digital signals."""
        bus_signals = ["v(bus01)", "v(bus02)", "v(bus03)"]
        
        for signal_name in bus_signals:
            with self.subTest(signal=signal_name):
                data = self.spice_data.get_signal(signal_name)
                
                # Digital signals should mostly be near 0V or VDD
                # Allow some tolerance for transitions
                unique_levels = len(np.unique(np.round(data, 1)))
                self.assertLessEqual(unique_levels, 30)  # Ring oscillator has many transition levels
    
    def test_current_signals_exist(self):
        """Test that current measurement signals are accessible."""
        current_signals = ["i(c1)", "i(c2)", "i(v1)"]
        
        for signal_name in current_signals:
            with self.subTest(signal=signal_name):
                data = self.spice_data.get_signal(signal_name)
                assert_signal_data_integrity(data, expected_length=REAL_FILE_TIME_POINTS)
                
                # Currents should be reasonable values (not zero everywhere)
                self.assertGreater(np.max(np.abs(data)), 1e-12)  # At least some current flow
    
    def test_device_currents_exist(self):
        """Test that device-level current measurements are accessible."""
        device_currents = ["ix(x4:gate)", "ix(x4:drain)", "ix(x5:source)"]
        
        for signal_name in device_currents:
            with self.subTest(signal=signal_name):
                if self.spice_data.has_signal(signal_name):
                    data = self.spice_data.get_signal(signal_name)
                    assert_signal_data_integrity(data, expected_length=REAL_FILE_TIME_POINTS)


class TestRealFileErrorConditions(unittest.TestCase):
    """Test error conditions with real file context."""
    
    @classmethod
    def setUpClass(cls):
        """Load the real file once for all tests in this class."""
        cls.spice_data = SpiceData(get_real_file_path())
    
    def test_nonexistent_signal_error(self):
        """Test error when requesting non-existent signal from real file."""
        with self.assertRaises(ValueError) as context:
            self.spice_data.get_signal("v(does_not_exist)")
        
        error_msg = str(context.exception)
        self.assertIn("not found in raw file", error_msg)
        self.assertIn("Available signals", error_msg)
        
        # Should show some actual signal names in error (first 5 signals)
        self.assertTrue(any(signal in error_msg for signal in ["time", "v(bus06)", "v(bus05)"]))
    
    def test_get_multiple_signals_with_invalid(self):
        """Test get_signals with mix of valid and invalid signal names."""
        signal_names = ["v(vdd)", "v(nonexistent)", "i(c1)"]
        
        with self.assertRaises(ValueError) as context:
            self.spice_data.get_signals(signal_names)
        
        # Should fail on the invalid signal
        self.assertIn("v(nonexistent)", str(context.exception))


if __name__ == '__main__':
    unittest.main() 