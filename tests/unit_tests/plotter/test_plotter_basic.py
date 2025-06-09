"""
Unit tests for SpicePlotter basic functionality.

This module tests the core API, initialization, method chaining, 
and property access for the SpicePlotter class.
"""

import unittest
from unittest.mock import Mock, patch
import numpy as np

from wave_view.core.plotter import SpicePlotter
from wave_view.core.config import PlotConfig
from . import create_mock_spice_data, create_basic_config


class TestSpicePlotterInitialization(unittest.TestCase):
    """Test SpicePlotter initialization and basic setup."""
    
    def test_init_without_raw_file(self):
        """Test initialization without raw file parameter."""
        plotter = SpicePlotter()
        
        # Check initial state
        self.assertIsNone(plotter.data)
        self.assertIsNone(plotter.config)
        self.assertEqual(len(plotter.processed_signals), 0)
        self.assertEqual(plotter._processed_signals, {})
    
    @patch('wave_view.core.plotter.SpiceData')
    def test_init_with_raw_file(self, mock_spice_data_class):
        """Test initialization with raw file parameter."""
        mock_spice_data_class.return_value = create_mock_spice_data()
        
        plotter = SpicePlotter("test.raw")
        
        # Check that data was loaded
        self.assertIsNotNone(plotter.data)
        mock_spice_data_class.assert_called_once_with("test.raw")
        self.assertIsNone(plotter.config)
        self.assertEqual(len(plotter.processed_signals), 0)
    
    @patch('wave_view.core.plotter.SpiceData')
    def test_init_with_invalid_raw_file(self, mock_spice_data_class):
        """Test initialization with invalid raw file."""
        mock_spice_data_class.side_effect = FileNotFoundError("File not found")
        
        with self.assertRaises(FileNotFoundError):
            SpicePlotter("nonexistent.raw")


class TestMethodChaining(unittest.TestCase):
    """Test fluent API method chaining."""
    
    @patch('wave_view.core.plotter.SpiceData')
    def test_load_data_returns_self(self, mock_spice_data_class):
        """Test that load_data returns self for chaining."""
        mock_spice_data_class.return_value = create_mock_spice_data()
        
        plotter = SpicePlotter()
        result = plotter.load_data("test.raw")
        
        self.assertIs(result, plotter)
        self.assertIsNotNone(plotter.data)
    
    def test_load_config_returns_self(self):
        """Test that load_config returns self for chaining."""
        plotter = SpicePlotter()
        config = create_basic_config()
        
        result = plotter.load_config(config)
        
        self.assertIs(result, plotter)
        self.assertIsNotNone(plotter.config)
    
    @patch('wave_view.core.plotter.SpiceData')
    def test_add_processed_signal_returns_self(self, mock_spice_data_class):
        """Test that add_processed_signal returns self for chaining."""
        mock_spice_data_class.return_value = create_mock_spice_data()
        
        plotter = SpicePlotter()
        plotter.load_data("test.raw")
        
        result = plotter.add_processed_signal("test", lambda d: d["v(vdd)"] * 2)
        
        self.assertIs(result, plotter)
        self.assertIn("test", plotter.processed_signals)
    
    @patch('wave_view.core.plotter.SpiceData')
    def test_method_chaining_complete_workflow(self, mock_spice_data_class):
        """Test complete workflow with method chaining."""
        mock_spice_data_class.return_value = create_mock_spice_data()
        
        config = create_basic_config()
        
        # Test chaining multiple methods
        result = (SpicePlotter()
                 .load_data("test.raw")
                 .load_config(config)
                 .add_processed_signal("doubled", lambda d: d["v(vdd)"] * 2))
        
        self.assertIsInstance(result, SpicePlotter)
        self.assertIsNotNone(result.data)
        self.assertIsNotNone(result.config)
        self.assertIn("doubled", result.processed_signals)


class TestDataAndConfigLoading(unittest.TestCase):
    """Test data and configuration loading functionality."""
    
    @patch('wave_view.core.plotter.SpiceData')
    def test_load_data_basic(self, mock_spice_data_class):
        """Test basic data loading functionality."""
        mock_data = create_mock_spice_data()
        mock_spice_data_class.return_value = mock_data
        
        plotter = SpicePlotter()
        plotter.load_data("test.raw")
        
        self.assertIs(plotter.data, mock_data)
        mock_spice_data_class.assert_called_once_with("test.raw")
    
    def test_load_config_from_plot_config_instance(self):
        """Test loading configuration from PlotConfig instance."""
        plotter = SpicePlotter()
        config = create_basic_config()
        
        plotter.load_config(config)
        
        self.assertIs(plotter.config, config)
    
    def test_load_config_from_dictionary(self):
        """Test loading configuration from dictionary."""
        plotter = SpicePlotter()
        config_dict = {
            "title": "Dict Config Test",
            "X": {"signal_key": "raw.time"},
            "Y": [{"label": "Test", "signals": {"TEST": "v(test)"}}]
        }
        
        plotter.load_config(config_dict)
        
        self.assertIsNotNone(plotter.config)
        self.assertIsInstance(plotter.config, PlotConfig)
        self.assertEqual(plotter.config.config["title"], "Dict Config Test")
    
    def test_load_config_invalid_type(self):
        """Test loading configuration with invalid type."""
        plotter = SpicePlotter()
        
        with self.assertRaises(ValueError):
            plotter.load_config(12345)  # Invalid config type


class TestProperties(unittest.TestCase):
    """Test property access and behavior."""
    
    @patch('wave_view.core.plotter.SpiceData')
    def test_data_property(self, mock_spice_data_class):
        """Test data property access."""
        mock_data = create_mock_spice_data()
        mock_spice_data_class.return_value = mock_data
        
        plotter = SpicePlotter()
        
        # Initially None
        self.assertIsNone(plotter.data)
        
        # After loading data
        plotter.load_data("test.raw")
        self.assertIs(plotter.data, mock_data)
    
    def test_config_property(self):
        """Test config property access."""
        plotter = SpicePlotter()
        config = create_basic_config()
        
        # Initially None
        self.assertIsNone(plotter.config)
        
        # After loading config
        plotter.load_config(config)
        self.assertIs(plotter.config, config)
    
    @patch('wave_view.core.plotter.SpiceData')
    def test_processed_signals_property(self, mock_spice_data_class):
        """Test processed signals property access."""
        mock_spice_data_class.return_value = create_mock_spice_data()
        
        plotter = SpicePlotter()
        plotter.load_data("test.raw")
        
        # Initially empty
        self.assertEqual(len(plotter.processed_signals), 0)
        self.assertEqual(plotter.processed_signals, {})
        
        # After adding processed signal
        plotter.add_processed_signal("power", lambda d: d["v(vdd)"] * d["i(vdd)"])
        
        processed = plotter.processed_signals
        self.assertEqual(len(processed), 1)
        self.assertIn("power", processed)
        self.assertIsInstance(processed["power"], np.ndarray)
        
        # The property returns a copy of the dict, but numpy arrays are still referenced
        # This is expected behavior - the dict is copied but arrays are shared
        processed_again = plotter.processed_signals
        self.assertIsNot(processed, processed_again)  # Different dict objects
        self.assertIs(processed["power"], processed_again["power"])  # Same numpy array


class TestStringRepresentation(unittest.TestCase):
    """Test string representation (__repr__) functionality."""
    
    def test_repr_initial_state(self):
        """Test __repr__ for initial empty state."""
        plotter = SpicePlotter()
        repr_str = repr(plotter)
        
        self.assertIn("SpicePlotter", repr_str)
        self.assertIn("no data", repr_str)
        self.assertIn("no config", repr_str)
        self.assertIn("no processed signals", repr_str)
    
    @patch('wave_view.core.plotter.SpiceData')
    def test_repr_with_data_only(self, mock_spice_data_class):
        """Test __repr__ with only data loaded."""
        mock_spice_data_class.return_value = create_mock_spice_data()
        
        plotter = SpicePlotter("test.raw")
        repr_str = repr(plotter)
        
        self.assertIn("SpicePlotter", repr_str)
        self.assertIn("data loaded", repr_str)
        self.assertIn("no config", repr_str)
        self.assertIn("no processed signals", repr_str)
    
    @patch('wave_view.core.plotter.SpiceData')
    def test_repr_with_data_and_config(self, mock_spice_data_class):
        """Test __repr__ with data and config loaded."""
        mock_spice_data_class.return_value = create_mock_spice_data()
        
        plotter = SpicePlotter("test.raw")
        plotter.load_config(create_basic_config())
        repr_str = repr(plotter)
        
        self.assertIn("SpicePlotter", repr_str)
        self.assertIn("data loaded", repr_str)
        self.assertIn("config loaded", repr_str)
        self.assertIn("no processed signals", repr_str)
    
    @patch('wave_view.core.plotter.SpiceData')
    def test_repr_complete_state(self, mock_spice_data_class):
        """Test __repr__ with all components loaded."""
        mock_spice_data_class.return_value = create_mock_spice_data()
        
        plotter = SpicePlotter("test.raw")
        plotter.load_config(create_basic_config())
        plotter.add_processed_signal("power", lambda d: d["v(vdd)"] * d["i(vdd)"])
        plotter.add_processed_signal("rms", lambda d: np.sqrt(np.mean(d["v(out)"]**2)))
        
        repr_str = repr(plotter)
        
        self.assertIn("SpicePlotter", repr_str)
        self.assertIn("data loaded", repr_str)
        self.assertIn("config loaded", repr_str)
        self.assertIn("2 processed signals", repr_str)


if __name__ == '__main__':
    unittest.main() 