"""
Unit tests for PlotConfig class in config.py.

This module tests the configuration management functionality including
YAML loading, validation, and multi-figure support.
"""

import unittest
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch
import yaml

from wave_view.core.config import PlotConfig


class TestPlotConfigInitialization(unittest.TestCase):
    """Test PlotConfig initialization from various sources."""
    
    def test_init_from_dictionary_single_figure(self):
        """Test creating config from dictionary (single figure)."""
        config_dict = {
            "title": "Test Plot",
            "X": {"signal_key": "raw.time", "label": "Time (s)"},
            "Y": [{"label": "Voltage", "signals": {"VDD": "v(vdd)"}}]
        }
        
        config = PlotConfig(config_dict)
        self.assertEqual(config.figure_count, 1)
        self.assertFalse(config.is_multi_figure)
        self.assertEqual(config.config["title"], "Test Plot")
        self.assertEqual(config.config["X"]["signal_key"], "raw.time")
        self.assertEqual(len(config.config["Y"]), 1)
    
    def test_init_from_list_multi_figure(self):
        """Test creating config from list (multi-figure)."""
        config_list = [
            {
                "title": "Figure 1",
                "X": {"signal_key": "raw.time", "label": "Time (s)"},
                "Y": [{"label": "V1", "signals": {"VDD": "v(vdd)"}}]
            },
            {
                "title": "Figure 2", 
                "X": {"signal_key": "raw.time", "label": "Time (s)"},
                "Y": [{"label": "V2", "signals": {"OUT": "v(out)"}}]
            }
        ]
        
        config = PlotConfig(config_list)
        self.assertEqual(config.figure_count, 2)
        self.assertTrue(config.is_multi_figure)
        self.assertEqual(config.get_figure_config(0)["title"], "Figure 1")
        self.assertEqual(config.get_figure_config(1)["title"], "Figure 2")
    
    def test_init_from_yaml_string(self):
        """Test creating config from YAML string content."""
        yaml_content = """
        title: "YAML String Test"
        X:
          signal_key: "raw.time"
          label: "Time (s)"
        Y:
          - label: "Voltage"
            signals:
              VDD: "v(vdd)"
        """
        
        config = PlotConfig(yaml_content)
        self.assertFalse(config.is_multi_figure)
        self.assertEqual(config.config["title"], "YAML String Test")
        self.assertEqual(config.config["X"]["signal_key"], "raw.time")
    
    def test_init_invalid_type(self):
        """Test initialization with invalid input type."""
        with self.assertRaises(ValueError) as context:
            PlotConfig(12345)  # Invalid type
        
        self.assertIn("Config source must be str, Path, dict, or list", str(context.exception))
        
        with self.assertRaises(ValueError) as context:
            PlotConfig(None)  # None is invalid
        
        self.assertIn("Config source must be str, Path, dict, or list", str(context.exception))


class TestFilePathDetection(unittest.TestCase):
    """Test the _looks_like_file_path method."""
    
    def test_looks_like_file_path_extensions(self):
        """Test file path detection with common extensions."""
        config = PlotConfig({"X": {"signal_key": "raw.time"}, "Y": []})
        
        # These should be detected as file paths
        self.assertTrue(config._looks_like_file_path("config.yaml"))
        self.assertTrue(config._looks_like_file_path("my_config.yml"))
        self.assertTrue(config._looks_like_file_path("data.json"))
        self.assertTrue(config._looks_like_file_path("path/to/config.yaml"))
        self.assertTrue(config._looks_like_file_path("./relative/config.yaml"))
    
    def test_looks_like_yaml_content(self):
        """Test YAML content detection."""
        config = PlotConfig({"X": {"signal_key": "raw.time"}, "Y": []})
        
        # These should be detected as YAML content
        self.assertFalse(config._looks_like_file_path("title: Test\nX: {signal_key: raw.time}"))
        self.assertFalse(config._looks_like_file_path("X:\n  signal_key: raw.time"))
        self.assertFalse(config._looks_like_file_path("- title: Figure 1"))
        self.assertFalse(config._looks_like_file_path("signals: {VDD: v(vdd)}"))
    
    def test_looks_like_file_path_edge_cases(self):
        """Test edge cases for file path detection."""
        config = PlotConfig({"X": {"signal_key": "raw.time"}, "Y": []})
        
        # Short strings without YAML syntax should be file paths
        self.assertTrue(config._looks_like_file_path("config"))
        self.assertTrue(config._looks_like_file_path("my_file"))
        
        # Strings with colons but no newlines could go either way
        # The implementation treats them as YAML content if they contain colons
        self.assertFalse(config._looks_like_file_path("title: Test Plot"))
        
        # Paths with directories
        self.assertTrue(config._looks_like_file_path("/absolute/path/config.yaml"))
        self.assertTrue(config._looks_like_file_path("relative/path"))


class TestFileBasedInitialization(unittest.TestCase):
    """Test PlotConfig initialization from files and Path objects."""
    
    def test_init_from_yaml_file(self):
        """Test creating config from YAML file."""
        config_content = """
        title: "Test YAML File"
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
            config = PlotConfig(temp_path)
            self.assertEqual(config.config["title"], "Test YAML File")
            self.assertFalse(config.is_multi_figure)
            self.assertEqual(config.config["X"]["signal_key"], "raw.time")
        finally:
            os.unlink(temp_path)
    
    def test_init_from_path_object(self):
        """Test creating config from Path object."""
        config_content = """
        title: "Path Object Test"
        X:
          signal_key: "raw.time"
        Y:
          - label: "Test"
            signals:
              TEST: "v(test)"
        """
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write(config_content)
            temp_path = Path(f.name)
        
        try:
            config = PlotConfig(temp_path)
            self.assertEqual(config.config["title"], "Path Object Test")
            self.assertFalse(config.is_multi_figure)
        finally:
            os.unlink(temp_path)
    
    def test_init_nonexistent_file(self):
        """Test initialization with non-existent file."""
        with self.assertRaises(FileNotFoundError) as context:
            PlotConfig("nonexistent_config.yaml")
        
        self.assertIn("Configuration file not found", str(context.exception))
    
    def test_init_invalid_yaml_file(self):
        """Test initialization with invalid YAML file."""
        invalid_yaml = """
        title: "Invalid YAML
        X: {
          signal_key: "raw.time"
          # Missing closing brace
        """
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write(invalid_yaml)
            temp_path = f.name
        
        try:
            with self.assertRaises(yaml.YAMLError) as context:
                PlotConfig(temp_path)
            
            self.assertIn("Invalid YAML in config file", str(context.exception))
        finally:
            os.unlink(temp_path)
    
    def test_init_invalid_yaml_string(self):
        """Test initialization with invalid YAML string content."""
        invalid_yaml_string = """
        title: "Invalid YAML String
        X: {
          signal_key: "raw.time"
          # Missing closing brace and quote
        """
        
        with self.assertRaises(yaml.YAMLError) as context:
            PlotConfig(invalid_yaml_string)
        
        self.assertIn("Invalid YAML content", str(context.exception))


class TestConfigurationStructureValidation(unittest.TestCase):
    """Test configuration structure validation and properties."""
    
    def test_valid_single_figure_config(self):
        """Test valid single figure configuration."""
        config_dict = {
            "title": "Valid Config",
            "X": {"signal_key": "raw.time", "label": "Time (s)"},
            "Y": [
                {"label": "Voltage", "signals": {"VDD": "v(vdd)"}},
                {"label": "Current", "signals": {"IDD": "i(vdd)"}}
            ]
        }
        
        config = PlotConfig(config_dict)
        self.assertFalse(config.is_multi_figure)
        self.assertEqual(config.figure_count, 1)
        
        # Test get_figure_config
        fig_config = config.get_figure_config(0)
        self.assertEqual(fig_config["title"], "Valid Config")
        self.assertEqual(len(fig_config["Y"]), 2)
    
    def test_valid_multi_figure_config(self):
        """Test valid multi-figure configuration."""
        config_list = [
            {
                "title": "Figure 1", 
                "X": {"signal_key": "raw.time"},
                "Y": [{"label": "V1", "signals": {"A": "v(a)"}}]
            },
            {
                "title": "Figure 2",
                "X": {"signal_key": "raw.freq"}, 
                "Y": [{"label": "V2", "signals": {"B": "v(b)"}}]
            }
        ]
        
        config = PlotConfig(config_list)
        self.assertTrue(config.is_multi_figure)
        self.assertEqual(config.figure_count, 2)
        
        # Test individual figure configs
        fig1 = config.get_figure_config(0)
        fig2 = config.get_figure_config(1)
        self.assertEqual(fig1["title"], "Figure 1")
        self.assertEqual(fig2["title"], "Figure 2")
        self.assertEqual(fig1["X"]["signal_key"], "raw.time")
        self.assertEqual(fig2["X"]["signal_key"], "raw.freq")
    
    def test_invalid_multi_figure_structure(self):
        """Test invalid multi-figure configuration structure."""
        # List containing non-dict elements
        invalid_config = [
            {"title": "Valid Figure", "X": {"signal_key": "raw.time"}, "Y": []},
            "invalid_string_element",  # This should cause error
            {"title": "Another Valid", "X": {"signal_key": "raw.time"}, "Y": []}
        ]
        
        with self.assertRaises(ValueError) as context:
            PlotConfig(invalid_config)
        
        self.assertIn("Figure 1 configuration must be a dictionary", str(context.exception))
    
    def test_get_figure_config_index_errors(self):
        """Test index errors for get_figure_config."""
        # Single figure config
        single_config = PlotConfig({"X": {"signal_key": "raw.time"}, "Y": []})
        
        # Valid index
        fig_config = single_config.get_figure_config(0)
        self.assertIsNotNone(fig_config)
        
        # Invalid index for single figure
        with self.assertRaises(IndexError):
            single_config.get_figure_config(1)
        
        # Multi-figure config
        multi_config = PlotConfig([
            {"X": {"signal_key": "raw.time"}, "Y": []},
            {"X": {"signal_key": "raw.freq"}, "Y": []}
        ])
        
        # Valid indices
        fig1 = multi_config.get_figure_config(0)
        fig2 = multi_config.get_figure_config(1)
        self.assertIsNotNone(fig1)
        self.assertIsNotNone(fig2)
        
        # Invalid index for multi-figure
        with self.assertRaises(IndexError):
            multi_config.get_figure_config(2)
    
    def test_config_property_access(self):
        """Test accessing configuration properties."""
        config_dict = {"title": "Test", "X": {"signal_key": "raw.time"}, "Y": []}
        config = PlotConfig(config_dict)
        
        # Test config property returns copy
        raw_config = config.config
        self.assertEqual(raw_config["title"], "Test")
        
        # Test to_dict method
        dict_config = config.to_dict()
        self.assertEqual(dict_config["title"], "Test")
    
    def test_config_repr(self):
        """Test string representation of PlotConfig."""
        # Single figure
        single_config = PlotConfig({"title": "My Plot", "X": {"signal_key": "raw.time"}, "Y": []})
        repr_str = repr(single_config)
        self.assertIn("PlotConfig", repr_str)
        self.assertIn("My Plot", repr_str)
        
        # Multi-figure
        multi_config = PlotConfig([
            {"title": "Fig1", "X": {"signal_key": "raw.time"}, "Y": []},
            {"title": "Fig2", "X": {"signal_key": "raw.time"}, "Y": []}
        ])
        repr_str = repr(multi_config)
        self.assertIn("PlotConfig", repr_str)
        self.assertIn("2 figures", repr_str)


class TestConfigurationValidation(unittest.TestCase):
    """Test configuration validation functionality."""
    
    def test_validate_without_spice_data(self):
        """Test basic configuration validation without SPICE data."""
        # Valid configuration
        valid_config = {
            "title": "Valid Config",
            "X": {"signal_key": "raw.time", "label": "Time"},
            "Y": [
                {"label": "Voltage", "signals": {"VDD": "v(vdd)"}},
                {"label": "Current", "signals": {"IDD": "i(vdd)"}}
            ]
        }
        
        config = PlotConfig(valid_config)
        warnings = config.validate()
        self.assertEqual(len(warnings), 0)
    
    def test_validate_missing_required_fields(self):
        """Test validation with missing required fields."""
        # Missing X configuration
        missing_x = {
            "title": "Missing X",
            "Y": [{"label": "Voltage", "signals": {"VDD": "v(vdd)"}}]
        }
        
        config = PlotConfig(missing_x)
        warnings = config.validate()
        self.assertGreater(len(warnings), 0)
        self.assertTrue(any("Missing required 'X'" in w for w in warnings))
        
        # Missing Y configuration
        missing_y = {
            "title": "Missing Y",
            "X": {"signal_key": "raw.time"}
        }
        
        config = PlotConfig(missing_y)
        warnings = config.validate()
        self.assertGreater(len(warnings), 0)
        self.assertTrue(any("Missing required 'Y'" in w for w in warnings))
        
        # Invalid X configuration (missing signal_key)
        invalid_x = {
            "title": "Invalid X",
            "X": {"label": "Time"},  # Missing signal_key
            "Y": [{"label": "V", "signals": {"VDD": "v(vdd)"}}]
        }
        
        config = PlotConfig(invalid_x)
        warnings = config.validate()
        self.assertGreater(len(warnings), 0)
        self.assertTrue(any("X configuration must have 'signal_key'" in w for w in warnings))
    
    def test_validate_invalid_y_configuration(self):
        """Test validation with invalid Y configuration."""
        # Y is not a list
        invalid_y_type = {
            "X": {"signal_key": "raw.time"},
            "Y": {"not": "a list"}  # Should be a list
        }
        
        config = PlotConfig(invalid_y_type)
        warnings = config.validate()
        self.assertGreater(len(warnings), 0)
        self.assertTrue(any("Y configuration must be a list" in w for w in warnings))
        
        # Y contains non-dict elements
        invalid_y_elements = {
            "X": {"signal_key": "raw.time"},
            "Y": [
                {"label": "Valid", "signals": {"VDD": "v(vdd)"}},
                "invalid_string",  # Should be a dict
                {"label": "Also Valid", "signals": {"OUT": "v(out)"}}
            ]
        }
        
        config = PlotConfig(invalid_y_elements)
        warnings = config.validate()
        self.assertGreater(len(warnings), 0)
        self.assertTrue(any("Y[1] must be a dictionary" in w for w in warnings))
        
        # Y element missing signals
        missing_signals = {
            "X": {"signal_key": "raw.time"},
            "Y": [
                {"label": "Missing Signals"}  # No 'signals' key
            ]
        }
        
        config = PlotConfig(missing_signals)
        warnings = config.validate()
        self.assertGreater(len(warnings), 0)
        self.assertTrue(any("Y[0] missing 'signals'" in w for w in warnings))
        
        # Y element with invalid signals format
        invalid_signals = {
            "X": {"signal_key": "raw.time"},
            "Y": [
                {"label": "Invalid Signals", "signals": "should_be_dict"}
            ]
        }
        
        config = PlotConfig(invalid_signals)
        warnings = config.validate()
        self.assertGreater(len(warnings), 0)
        self.assertTrue(any("Y[0]['signals'] must be a dictionary" in w for w in warnings))
    
    def test_validate_multi_figure_configuration(self):
        """Test validation with multi-figure configuration."""
        multi_config = [
            {
                "title": "Figure 1",
                "X": {"signal_key": "raw.time"},
                "Y": [{"label": "V1", "signals": {"VDD": "v(vdd)"}}]
            },
            {
                "title": "Figure 2",
                # Missing X configuration - should generate warning
                "Y": [{"label": "V2", "signals": {"OUT": "v(out)"}}]
            }
        ]
        
        config = PlotConfig(multi_config)
        warnings = config.validate()
        self.assertGreater(len(warnings), 0)
        self.assertTrue(any("Figure 1: Missing required 'X'" in w for w in warnings))
    
    def test_validate_with_mocked_spice_data(self):
        """Test validation against mocked SPICE data."""
        # Create a mock SPICE data object
        mock_spice_data = Mock()
        mock_spice_data.signals = ["time", "v(vdd)", "v(out)", "i(vdd)"]
        
        # Configuration with valid signals
        valid_config = {
            "X": {"signal_key": "raw.time"},
            "Y": [
                {"label": "Voltage", "signals": {"VDD": "v(vdd)", "OUT": "v(out)"}},
                {"label": "Current", "signals": {"IDD": "i(vdd)"}}
            ]
        }
        
        config = PlotConfig(valid_config)
        warnings = config.validate(mock_spice_data)
        self.assertEqual(len(warnings), 0)
        
        # Configuration with invalid signals
        invalid_config = {
            "X": {"signal_key": "raw.nonexistent"},  # Signal doesn't exist
            "Y": [
                {"label": "Invalid", "signals": {"MISSING": "v(missing)"}}
            ]
        }
        
        config = PlotConfig(invalid_config)
        warnings = config.validate(mock_spice_data)
        self.assertGreater(len(warnings), 0)
        self.assertTrue(any("nonexistent" in w for w in warnings))
        self.assertTrue(any("missing" in w for w in warnings))
    
    def test_validate_with_processed_signals(self):
        """Test validation with processed signals (data. prefix)."""
        mock_spice_data = Mock()
        mock_spice_data.signals = ["time", "v(vdd)", "v(out)"]
        
        # Configuration using processed signals
        config_with_processed = {
            "X": {"signal_key": "raw.time"},
            "Y": [
                {"label": "Raw", "signals": {"VDD": "v(vdd)"}},
                {"label": "Processed", "signals": {"POWER": "data.power"}}  # Processed signal
            ]
        }
        
        config = PlotConfig(config_with_processed)
        warnings = config.validate(mock_spice_data)
        # Processed signals can't be validated without context, so no warnings expected for them
        # But raw signals should still be validated
        self.assertEqual(len(warnings), 0)


class TestTemplatesAndRawFilePathHandling(unittest.TestCase):
    """Test template system and raw file path handling."""
    
    def test_from_template_basic(self):
        """Test creating config from basic template."""
        config = PlotConfig.from_template("basic")
        
        self.assertFalse(config.is_multi_figure)
        self.assertIn("title", config.config)
        self.assertIn("X", config.config)
        self.assertIn("Y", config.config)
        self.assertEqual(config.config["X"]["signal_key"], "raw.time")
        self.assertIsInstance(config.config["Y"], list)
    
    def test_from_template_invalid(self):
        """Test creating config from invalid template name."""
        with self.assertRaises(ValueError) as context:
            PlotConfig.from_template("nonexistent_template")
        
        self.assertIn("Template 'nonexistent_template' not found", str(context.exception))
        self.assertIn("Available:", str(context.exception))
    
    def test_get_raw_file_path_single_figure(self):
        """Test getting raw file path from single figure config."""
        # Config with source
        config_with_source = {
            "source": "./test_file.raw",
            "X": {"signal_key": "raw.time"},
            "Y": []
        }
        
        config = PlotConfig(config_with_source)
        raw_path = config.get_raw_file_path()
        self.assertEqual(raw_path, "./test_file.raw")
        
        # Config without source
        config_no_source = {
            "X": {"signal_key": "raw.time"},
            "Y": []
        }
        
        config = PlotConfig(config_no_source)
        raw_path = config.get_raw_file_path()
        self.assertIsNone(raw_path)
    
    def test_get_raw_file_path_multi_figure(self):
        """Test getting raw file path from multi-figure config."""
        multi_config = [
            {
                "title": "Figure 1",
                "source": "./file1.raw",
                "X": {"signal_key": "raw.time"},
                "Y": []
            },
            {
                "title": "Figure 2", 
                "source": "./file2.raw",
                "X": {"signal_key": "raw.time"},
                "Y": []
            }
        ]
        
        config = PlotConfig(multi_config)
        path1 = config.get_raw_file_path(0)
        path2 = config.get_raw_file_path(1)
        
        self.assertEqual(path1, "./file1.raw")
        self.assertEqual(path2, "./file2.raw")
        
        # Test invalid index
        with self.assertRaises(IndexError):
            config.get_raw_file_path(2)
    
    def test_get_raw_file_path_relative_resolution(self):
        """Test relative path resolution when config loaded from file."""
        config_content = """
        source: "./relative_file.raw"
        X:
          signal_key: "raw.time"
        Y: []
        """
        
        # Create a config file in a subdirectory
        with tempfile.TemporaryDirectory() as temp_dir:
            config_dir = Path(temp_dir) / "config_subdir"
            config_dir.mkdir()
            
            config_file = config_dir / "test_config.yaml"
            with open(config_file, 'w') as f:
                f.write(config_content)
            
            config = PlotConfig(config_file)
            raw_path = config.get_raw_file_path()
            
            # Should resolve relative to config file location
            expected_path = str(config_dir / "relative_file.raw")
            self.assertEqual(raw_path, expected_path)


class TestLogScaleSupport(unittest.TestCase):
    """Test configuration support for log scale features."""
    
    def test_config_with_x_axis_log_scale(self):
        """Test configuration with X-axis log scale."""
        config_dict = {
            "title": "Log X Scale Test",
            "X": {
                "signal_key": "raw.frequency",
                "label": "Frequency (Hz)",
                "scale": "log"
            },
            "Y": [
                {"label": "Magnitude", "signals": {"MAG": "v(out)"}}
            ]
        }
        
        config = PlotConfig(config_dict)
        warnings = config.validate()
        self.assertEqual(len(warnings), 0)
        
        fig_config = config.get_figure_config(0)
        self.assertEqual(fig_config["X"]["scale"], "log")
    
    def test_config_with_y_axis_log_scale(self):
        """Test configuration with Y-axis log scale."""
        config_dict = {
            "title": "Log Y Scale Test",
            "X": {"signal_key": "raw.time", "label": "Time (s)"},
            "Y": [
                {
                    "label": "Power (W)",
                    "scale": "log",
                    "signals": {"POWER": "data.power"}
                },
                {
                    "label": "Linear Voltage",
                    "signals": {"VDD": "v(vdd)"}
                }
            ]
        }
        
        config = PlotConfig(config_dict)
        warnings = config.validate()
        self.assertEqual(len(warnings), 0)
        
        fig_config = config.get_figure_config(0)
        self.assertEqual(fig_config["Y"][0]["scale"], "log")
        self.assertNotIn("scale", fig_config["Y"][1])  # Second Y-axis doesn't have scale
    
    def test_config_with_both_axes_log_scale(self):
        """Test configuration with both X and Y axes log scale."""
        config_dict = {
            "title": "Both Axes Log Scale",
            "X": {
                "signal_key": "raw.frequency",
                "label": "Frequency (Hz)",
                "scale": "log"
            },
            "Y": [
                {
                    "label": "Magnitude (dB)",
                    "scale": "log",
                    "signals": {"MAG_DB": "data.mag_db"}
                }
            ]
        }
        
        config = PlotConfig(config_dict)
        warnings = config.validate()
        self.assertEqual(len(warnings), 0)
        
        fig_config = config.get_figure_config(0)
        self.assertEqual(fig_config["X"]["scale"], "log")
        self.assertEqual(fig_config["Y"][0]["scale"], "log")
    
    def test_config_with_mixed_y_axis_scales(self):
        """Test configuration with mixed linear and log Y-axes."""
        config_dict = {
            "title": "Mixed Y Scales",
            "X": {"signal_key": "raw.frequency", "label": "Frequency (Hz)"},
            "Y": [
                {
                    "label": "Linear Scale",
                    "signals": {"LINEAR": "v(linear)"}
                },
                {
                    "label": "Log Scale",
                    "scale": "log",
                    "signals": {"LOG": "v(log)"}
                },
                {
                    "label": "Explicit Linear",
                    "scale": "linear",
                    "signals": {"EXPLICIT": "v(explicit)"}
                }
            ]
        }
        
        config = PlotConfig(config_dict)
        warnings = config.validate()
        self.assertEqual(len(warnings), 0)
        
        fig_config = config.get_figure_config(0)
        # First Y-axis: no scale specified (defaults to linear)
        self.assertNotIn("scale", fig_config["Y"][0])
        # Second Y-axis: log scale
        self.assertEqual(fig_config["Y"][1]["scale"], "log")
        # Third Y-axis: explicit linear scale
        self.assertEqual(fig_config["Y"][2]["scale"], "linear")


if __name__ == '__main__':
    unittest.main() 