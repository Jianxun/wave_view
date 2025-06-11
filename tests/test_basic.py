"""
Basic tests for Wave View core functionality.

These tests verify that the classes can be imported and instantiated correctly,
without requiring actual SPICE files.
"""

import unittest
from unittest.mock import Mock, patch
import numpy as np
import tempfile
import os

from wave_view.core.config import PlotConfig
from wave_view.core.plotter import SpicePlotter
from wave_view.api import config_from_yaml, config_from_file


class TestPlotConfig(unittest.TestCase):
    """Test PlotConfig class functionality."""
    
    def test_config_from_dict(self):
        """Test creating config from dictionary."""
        config_dict = {
            "title": "Test Plot",
            "X": {"signal_key": "raw.time", "label": "Time (s)"},
            "Y": [{"label": "Voltage", "signals": {"VDD": "v(vdd)"}}]
        }
        
        config = PlotConfig(config_dict)
        self.assertEqual(config.config["title"], "Test Plot")
        self.assertIn("X", config.config)
        self.assertIn("Y", config.config)
    
    def test_multi_figure_config(self):
        """Test multi-figure configuration rejection."""
        config_list = [
            {"title": "Figure 1", "X": {"signal_key": "raw.time"}, "Y": []},
            {"title": "Figure 2", "X": {"signal_key": "raw.time"}, "Y": []}
        ]
        
        # Multi-figure configurations should now be rejected
        with self.assertRaises(ValueError) as context:
            PlotConfig(config_list)
        
        self.assertIn("Multi-figure configurations are no longer supported", str(context.exception))
    
    def test_config_validation(self):
        """Test basic configuration validation."""
        # Valid config
        valid_config = {
            "X": {"signal_key": "raw.time"},
            "Y": [{"signals": {"test": "v(test)"}}]
        }
        config = PlotConfig(valid_config)
        warnings = config.validate()
        self.assertEqual(len(warnings), 0)
        
        # Invalid config - missing X
        invalid_config = {"Y": [{"signals": {"test": "v(test)"}}]}
        config = PlotConfig(invalid_config)
        warnings = config.validate()
        self.assertGreater(len(warnings), 0)
        self.assertTrue(any("Missing required 'X'" in w for w in warnings))
    
    def test_template_creation(self):
        """Test creating config from template."""
        config = PlotConfig.from_template("basic")
        self.assertIn("title", config.config)
        self.assertIn("X", config.config)
        self.assertIn("Y", config.config)
    
    def test_yaml_file_config(self):
        """Test loading config from YAML file using config_from_file."""
        config_content = """
        title: "Test YAML Config"
        X:
          signal_key: "raw.time"
          label: "Time (s)"
        Y:
          - label: "Voltage"
            signals:
              VDD: "v(vdd)"
        """
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write(config_content)
            temp_path = f.name
        
        try:
            config = config_from_file(temp_path)
            self.assertEqual(config.config["title"], "Test YAML Config")
            self.assertIn("X", config.config)
            self.assertIn("Y", config.config)
        finally:
            os.unlink(temp_path)


class TestSpicePlotter(unittest.TestCase):
    """Test SpicePlotter class functionality."""
    
    def test_plotter_initialization(self):
        """Test plotter can be initialized."""
        plotter = SpicePlotter()
        self.assertIsNone(plotter.data)
        self.assertIsNone(plotter.config)
        self.assertEqual(len(plotter.processed_signals), 0)
    
    def test_plotter_method_chaining(self):
        """Test that plotter methods return self for chaining."""
        plotter = SpicePlotter()
        
        # Mock SpiceData to avoid needing real files
        with patch('wave_view.core.plotter.SpiceData') as mock_spice_data:
            mock_instance = Mock()
            mock_instance.signals = ["time", "v(vdd)", "i(vdd)"]
            mock_instance.get_signal.return_value = np.array([1, 2, 3])
            mock_spice_data.return_value = mock_instance
            
            # Test method chaining
            result = plotter.load_data("test.raw")
            self.assertIs(result, plotter)
    
    def test_processed_signals(self):
        """Test adding processed signals."""
        plotter = SpicePlotter()
        
        # Mock SpiceData
        with patch('wave_view.core.plotter.SpiceData') as mock_spice_data:
            mock_instance = Mock()
            mock_instance.signals = ["time", "v(vdd)", "i(vdd)"]
            mock_instance.get_signal.side_effect = lambda name: {
                "time": np.array([0, 1, 2]),
                "v(vdd)": np.array([1.8, 1.8, 1.8]),
                "i(vdd)": np.array([0.1, 0.2, 0.3])
            }[name]
            mock_spice_data.return_value = mock_instance
            
            plotter.load_data("test.raw")
            
            # Add a processed signal
            plotter.add_processed_signal("power", lambda d: d["v(vdd)"] * d["i(vdd)"])
            
            # Check that processed signal was added
            processed = plotter.processed_signals
            self.assertIn("power", processed)
            np.testing.assert_array_almost_equal(processed["power"], np.array([0.18, 0.36, 0.54]), decimal=10)


class TestErrorHandling(unittest.TestCase):
    """Test error handling in core components."""
    
    def test_invalid_config_file(self):
        """Test handling of invalid config files using config_from_file."""
        with self.assertRaises(FileNotFoundError):
            config_from_file("nonexistent_config.yaml")
    
    def test_invalid_config_structure(self):
        """Test handling of invalid config structure."""
        with self.assertRaises(ValueError):
            PlotConfig(12345)  # Neither string, dict, list, nor Path
    
    def test_plotter_without_data(self):
        """Test plotter error when trying to create figure without data."""
        plotter = SpicePlotter()
        config = PlotConfig({"X": {"signal_key": "raw.time"}, "Y": []})
        plotter.load_config(config)
        
        with self.assertRaises(ValueError):
            plotter.create_figure()
    
    def test_plotter_without_config(self):
        """Test plotter error when trying to create figure without config."""
        plotter = SpicePlotter()
        
        with patch('wave_view.core.plotter.SpiceData'):
            plotter.load_data("test.raw")
            
            with self.assertRaises(ValueError):
                plotter.create_figure()


if __name__ == '__main__':
    # Set up test discovery
    loader = unittest.TestLoader()
    suite = loader.discover('.', pattern='test_*.py')
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite) 