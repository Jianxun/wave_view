"""
Unit tests for SpicePlotter processed signals functionality.

This module tests the processed signal features including signal computation,
storage, error handling, and integration with signal resolution.
"""

import unittest
from unittest.mock import Mock, patch
import numpy as np

from wave_view.core.plotter import SpicePlotter
from . import create_mock_spice_data, create_processed_signals_config


class TestProcessedSignalBasics(unittest.TestCase):
    """Test basic processed signal functionality."""
    
    @patch('wave_view.core.plotter.SpiceData')
    def test_add_simple_processed_signal(self, mock_spice_data_class):
        """Test adding a simple processed signal."""
        mock_spice_data_class.return_value = create_mock_spice_data()
        
        plotter = SpicePlotter("test.raw")
        
        # Add a simple processed signal
        result = plotter.add_processed_signal("doubled_vdd", lambda d: d["v(vdd)"] * 2)
        
        # Check method chaining
        self.assertIs(result, plotter)
        
        # Check signal was added
        processed = plotter.processed_signals
        self.assertIn("doubled_vdd", processed)
        self.assertIsInstance(processed["doubled_vdd"], np.ndarray)
        
        # Check computation correctness
        expected = create_mock_spice_data().get_signal("v(vdd)") * 2
        np.testing.assert_array_equal(processed["doubled_vdd"], expected)
    
    @patch('wave_view.core.plotter.SpiceData')
    def test_add_complex_processed_signal(self, mock_spice_data_class):
        """Test adding a complex processed signal involving multiple signals."""
        mock_spice_data_class.return_value = create_mock_spice_data()
        
        plotter = SpicePlotter("test.raw")
        
        # Add power calculation
        plotter.add_processed_signal("power", lambda d: d["v(vdd)"] * d["i(vdd)"])
        
        processed = plotter.processed_signals
        self.assertIn("power", processed)
        
        # Check computation
        vdd = create_mock_spice_data().get_signal("v(vdd)")
        idd = create_mock_spice_data().get_signal("i(vdd)")
        expected_power = vdd * idd
        np.testing.assert_array_equal(processed["power"], expected_power)
    
    @patch('wave_view.core.plotter.SpiceData')
    def test_add_mathematical_processed_signal(self, mock_spice_data_class):
        """Test adding processed signal with mathematical operations."""
        mock_spice_data_class.return_value = create_mock_spice_data()
        
        plotter = SpicePlotter("test.raw")
        
        # Add RMS calculation
        plotter.add_processed_signal("rms_out", lambda d: np.sqrt(np.mean(d["v(out)"]**2)))
        
        processed = plotter.processed_signals
        self.assertIn("rms_out", processed)
        
        # Check it's a scalar (converted to array)
        self.assertEqual(processed["rms_out"].shape, ())  # Scalar
        self.assertIsInstance(processed["rms_out"], np.ndarray)
    
    @patch('wave_view.core.plotter.SpiceData')
    def test_add_multiple_processed_signals(self, mock_spice_data_class):
        """Test adding multiple processed signals."""
        mock_spice_data_class.return_value = create_mock_spice_data()
        
        plotter = SpicePlotter("test.raw")
        
        # Add multiple signals
        plotter.add_processed_signal("power", lambda d: d["v(vdd)"] * d["i(vdd)"])
        plotter.add_processed_signal("neg_vdd", lambda d: -d["v(vdd)"])
        plotter.add_processed_signal("vout_squared", lambda d: d["v(out)"]**2)
        
        processed = plotter.processed_signals
        self.assertEqual(len(processed), 3)
        self.assertIn("power", processed)
        self.assertIn("neg_vdd", processed)
        self.assertIn("vout_squared", processed)


class TestProcessedSignalErrorHandling(unittest.TestCase):
    """Test error handling for processed signals."""
    
    def test_add_processed_signal_without_data(self):
        """Test adding processed signal without loading data first."""
        plotter = SpicePlotter()
        
        with self.assertRaises(ValueError) as context:
            plotter.add_processed_signal("test", lambda d: d["v(vdd)"] * 2)
        
        self.assertIn("Must load SPICE data before adding processed signals", str(context.exception))
    
    @patch('wave_view.core.plotter.SpiceData')
    def test_add_processed_signal_invalid_function(self, mock_spice_data_class):
        """Test adding processed signal with invalid function."""
        mock_spice_data_class.return_value = create_mock_spice_data()
        
        plotter = SpicePlotter("test.raw")
        
        # Function that references non-existent signal
        with self.assertRaises(ValueError) as context:
            plotter.add_processed_signal("invalid", lambda d: d["nonexistent_signal"])
        
        self.assertIn("Error computing processed signal 'invalid'", str(context.exception))
    
    @patch('wave_view.core.plotter.SpiceData')
    def test_add_processed_signal_function_exception(self, mock_spice_data_class):
        """Test adding processed signal with function that raises exception."""
        mock_spice_data_class.return_value = create_mock_spice_data()
        
        plotter = SpicePlotter("test.raw")
        
        # Function that raises an exception
        def bad_function(d):
            raise RuntimeError("Intentional error for testing")
        
        with self.assertRaises(ValueError) as context:
            plotter.add_processed_signal("bad", bad_function)
        
        self.assertIn("Error computing processed signal 'bad'", str(context.exception))
        self.assertIn("Intentional error for testing", str(context.exception))
    
    @patch('wave_view.core.plotter.SpiceData')
    def test_add_processed_signal_type_conversion(self, mock_spice_data_class):
        """Test that non-numpy array results are converted properly."""
        mock_spice_data_class.return_value = create_mock_spice_data()
        
        plotter = SpicePlotter("test.raw")
        
        # Function returning Python list
        plotter.add_processed_signal("list_signal", lambda d: [1, 2, 3, 4, 5])
        
        processed = plotter.processed_signals
        self.assertIn("list_signal", processed)
        self.assertIsInstance(processed["list_signal"], np.ndarray)
        self.assertEqual(processed["list_signal"].dtype, float)
        np.testing.assert_array_equal(processed["list_signal"], [1.0, 2.0, 3.0, 4.0, 5.0])


class TestProcessedSignalIntegration(unittest.TestCase):
    """Test integration of processed signals with other plotter functionality."""
    
    @patch('wave_view.core.plotter.SpiceData')
    def test_processed_signals_in_signal_resolution(self, mock_spice_data_class):
        """Test that processed signals can be resolved with 'data.' prefix."""
        mock_spice_data_class.return_value = create_mock_spice_data()
        
        plotter = SpicePlotter("test.raw")
        plotter.load_config(create_processed_signals_config())
        plotter.add_processed_signal("power", lambda d: d["v(vdd)"] * d["i(vdd)"])
        
        # Test the internal _get_signal_data method through create_figure
        try:
            fig = plotter.create_figure()
            
            # Should succeed without errors
            self.assertIsNotNone(fig)
            
            # Check that we have traces (indicating successful signal resolution)
            self.assertGreater(len(fig.data), 0)
        except Exception as e:
            self.fail(f"Figure creation failed with processed signals: {e}")
    
    @patch('wave_view.core.plotter.SpiceData')
    def test_processed_signal_not_found_in_config(self, mock_spice_data_class):
        """Test error when config references non-existent processed signal."""
        mock_spice_data_class.return_value = create_mock_spice_data()
        
        plotter = SpicePlotter("test.raw")
        plotter.load_config(create_processed_signals_config())
        # Note: Not adding the required "power" processed signal
        
        with self.assertRaises(ValueError) as context:
            plotter.create_figure()
        
        self.assertIn("Processed signal 'power' not found", str(context.exception))
    
    @patch('wave_view.core.plotter.SpiceData')
    def test_processed_signals_with_method_chaining(self, mock_spice_data_class):
        """Test processed signals with fluent API method chaining."""
        mock_spice_data_class.return_value = create_mock_spice_data()
        
        # Test complete workflow with method chaining
        plotter = (SpicePlotter()
                  .load_data("test.raw")
                  .load_config(create_processed_signals_config())
                  .add_processed_signal("power", lambda d: d["v(vdd)"] * d["i(vdd)"]))
        
        # Should be able to create figure
        fig = plotter.create_figure()
        self.assertIsNotNone(fig)
        self.assertGreater(len(fig.data), 0)
    
    @patch('wave_view.core.plotter.SpiceData')
    def test_overwrite_processed_signal(self, mock_spice_data_class):
        """Test overwriting an existing processed signal."""
        mock_spice_data_class.return_value = create_mock_spice_data()
        
        plotter = SpicePlotter("test.raw")
        
        # Add initial signal
        plotter.add_processed_signal("test_signal", lambda d: d["v(vdd)"] * 1)
        initial_value = plotter.processed_signals["test_signal"][0]
        
        # Overwrite with new calculation
        plotter.add_processed_signal("test_signal", lambda d: d["v(vdd)"] * 10)
        new_value = plotter.processed_signals["test_signal"][0]
        
        # Should be different values
        self.assertNotEqual(initial_value, new_value)
        self.assertEqual(new_value, initial_value * 10)


class TestProcessedSignalDataTypes(unittest.TestCase):
    """Test processed signals with different data types and edge cases."""
    
    @patch('wave_view.core.plotter.SpiceData')
    def test_processed_signal_boolean_result(self, mock_spice_data_class):
        """Test processed signal returning boolean array."""
        mock_spice_data_class.return_value = create_mock_spice_data()
        
        plotter = SpicePlotter("test.raw")
        
        # Boolean comparison
        plotter.add_processed_signal("vdd_high", lambda d: d["v(vdd)"] > 1.5)
        
        processed = plotter.processed_signals
        self.assertIn("vdd_high", processed)
        self.assertEqual(processed["vdd_high"].dtype, float)  # Converted to float
        
        # Check boolean logic is preserved
        vdd = create_mock_spice_data().get_signal("v(vdd)")
        expected = (vdd > 1.5).astype(float)
        np.testing.assert_array_equal(processed["vdd_high"], expected)
    
    @patch('wave_view.core.plotter.SpiceData')
    def test_processed_signal_complex_result(self, mock_spice_data_class):
        """Test processed signal returning complex numbers."""
        mock_spice_data_class.return_value = create_mock_spice_data()
        
        plotter = SpicePlotter("test.raw")
        
        # Complex signal (like FFT result)
        plotter.add_processed_signal("complex_signal", 
                                   lambda d: d["v(out)"] + 1j * d["v(vdd)"])
        
        processed = plotter.processed_signals
        self.assertIn("complex_signal", processed)
        # Should be converted to float (complex -> float conversion)
        self.assertEqual(processed["complex_signal"].dtype, float)
    
    @patch('wave_view.core.plotter.SpiceData')
    def test_processed_signal_empty_array(self, mock_spice_data_class):
        """Test processed signal returning empty array."""
        mock_spice_data_class.return_value = create_mock_spice_data()
        
        plotter = SpicePlotter("test.raw")
        
        # Empty array
        plotter.add_processed_signal("empty", lambda d: np.array([]))
        
        processed = plotter.processed_signals
        self.assertIn("empty", processed)
        self.assertEqual(len(processed["empty"]), 0)
        self.assertEqual(processed["empty"].dtype, float)
    
    @patch('wave_view.core.plotter.SpiceData')
    def test_processed_signal_single_value(self, mock_spice_data_class):
        """Test processed signal returning single scalar value."""
        mock_spice_data_class.return_value = create_mock_spice_data()
        
        plotter = SpicePlotter("test.raw")
        
        # Single value (like average)
        plotter.add_processed_signal("average", lambda d: np.mean(d["v(vdd)"]))
        
        processed = plotter.processed_signals
        self.assertIn("average", processed)
        self.assertEqual(processed["average"].shape, ())  # Scalar array
        self.assertEqual(processed["average"].dtype, float)


if __name__ == '__main__':
    unittest.main() 