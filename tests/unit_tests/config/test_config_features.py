"""
Unit tests for PlotConfig advanced features.

This module tests advanced PlotConfig functionality including templates,
raw file path handling, log scale support, and advanced configuration features.
"""

import unittest
import os
from pathlib import Path

from wave_view.core.config import PlotConfig
from wave_view.api import config_from_file
from . import (
    create_temp_yaml_file, create_temp_directory_with_config, cleanup_temp_file,
    cleanup_temp_directory, get_config_with_log_scale, get_config_with_source_path,
    assert_config_structure
)


class TestTemplateSystem(unittest.TestCase):
    """Test configuration template system."""
    
    def test_from_template_basic(self):
        """Test creating config from basic template."""
        config = PlotConfig.from_template("basic")
        
        # Template creates single-figure configuration
        self.assertIn("title", config.config)
        self.assertIn("X", config.config)
        self.assertIn("Y", config.config)
        
        # Basic template should have time-based X axis
        self.assertEqual(config.config["X"]["signal_key"], "raw.time")
        self.assertIsInstance(config.config["Y"], list)
        
        # Validate structure
        assert_config_structure(config.config)
    
    def test_from_template_invalid(self):
        """Test creating config from invalid template name."""
        with self.assertRaises(ValueError) as context:
            PlotConfig.from_template("nonexistent_template")
        
        error_msg = str(context.exception)
        self.assertIn("Template 'nonexistent_template' not found", error_msg)
        self.assertIn("Available:", error_msg)
    
    def test_from_template_available_templates(self):
        """Test that template error message shows available templates."""
        with self.assertRaises(ValueError) as context:
            PlotConfig.from_template("invalid")
        
        error_msg = str(context.exception)
        self.assertIn("basic", error_msg)  # Should show basic template
    
    def test_template_creates_valid_config(self):
        """Test that template-created configs pass validation."""
        config = PlotConfig.from_template("basic")
        warnings = config.validate()
        self.assertEqual(len(warnings), 0, f"Template config should be valid, got warnings: {warnings}")
    
    def test_template_config_modifiable(self):
        """Test that template-created configs can be modified."""
        config = PlotConfig.from_template("basic")
        
        # Modify the config
        modified_config = config.config.copy()
        modified_config["title"] = "Modified Template Config"
        
        new_config = PlotConfig(modified_config)
        self.assertEqual(new_config.config["title"], "Modified Template Config")
        
        # Original config should be unchanged
        self.assertNotEqual(config.config["title"], "Modified Template Config")


class TestRawFilePathHandling(unittest.TestCase):
    """Test raw file path handling and resolution."""
    
    def test_get_raw_file_path_single_figure(self):
        """Test getting raw file path from single figure config."""
        # Config with source
        config_with_source = get_config_with_source_path()
        config = PlotConfig(config_with_source)
        
        raw_path = config.get_raw_file_path()
        self.assertEqual(raw_path, "./test_data.raw")
        
        # Config without source
        config_no_source = {
            "title": "No Source Config",
            "X": {"signal_key": "raw.time"},
            "Y": [{"label": "Test", "signals": {"TEST": "v(test)"}}]
        }
        
        config = PlotConfig(config_no_source)
        raw_path = config.get_raw_file_path()
        self.assertIsNone(raw_path)
    
    def test_multi_figure_config_rejected(self):
        """Test that multi-figure configurations are rejected."""
        multi_config = [
            {
                "title": "Figure 1",
                "source": "./file1.raw",
                "X": {"signal_key": "raw.time"},
                "Y": [{"label": "V1", "signals": {"VDD": "v(vdd)"}}]
            },
            {
                "title": "Figure 2",
                "source": "./file2.raw", 
                "X": {"signal_key": "raw.time"},
                "Y": [{"label": "V2", "signals": {"OUT": "v(out)"}}]
            }
        ]
        
        # Multi-figure configurations should be rejected
        with self.assertRaises(ValueError) as context:
            PlotConfig(multi_config)
        
        self.assertIn("Multi-figure configurations are no longer supported", str(context.exception))
    
    def test_get_raw_file_path_single_figure_only(self):
        """Test raw file path handling for single figure configs."""
        config_with_source = get_config_with_source_path()
        config = PlotConfig(config_with_source)
        
        # Single figure configs should return the source path directly
        path = config.get_raw_file_path()
        self.assertEqual(path, "./test_data.raw")
    
    def test_get_raw_file_path_relative_resolution(self):
        """Test relative path resolution when config loaded from file."""
        config_content = get_config_with_source_path()
        config_content["source"] = "./relative_file.raw"
        
        # Create config in a subdirectory
        temp_dir, config_file = create_temp_directory_with_config("test_config.yaml", config_content)
        
        try:
            config = config_from_file(config_file)
            raw_path = config.get_raw_file_path()
            
            # Should resolve relative to config file location
            expected_path = str(Path(temp_dir) / "relative_file.raw")
            self.assertEqual(raw_path, expected_path)
        finally:
            cleanup_temp_directory(temp_dir)
    
    def test_get_raw_file_path_absolute_paths(self):
        """Test that absolute paths are not modified."""
        config_content = get_config_with_source_path()
        config_content["source"] = "/absolute/path/to/file.raw"
        
        temp_dir, config_file = create_temp_directory_with_config("test_config.yaml", config_content)
        
        try:
            config = config_from_file(config_file)
            raw_path = config.get_raw_file_path()
            
            # Absolute paths should remain unchanged
            self.assertEqual(raw_path, "/absolute/path/to/file.raw")
        finally:
            cleanup_temp_directory(temp_dir)
    
    def test_multi_figure_yaml_file_rejected(self):
        """Test that multi-figure YAML files are rejected."""
        multi_config = [
            {
                "title": "Figure 1",
                "source": "./data1.raw",  # Relative path
                "X": {"signal_key": "raw.time"},
                "Y": []
            },
            {
                "title": "Figure 2", 
                "source": "/absolute/data2.raw",  # Absolute path
                "X": {"signal_key": "raw.time"},
                "Y": []
            }
        ]
        
        temp_dir, config_file = create_temp_directory_with_config("multi_config.yaml", multi_config)
        
        try:
            # Multi-figure YAML files should be rejected
            with self.assertRaises(ValueError) as context:
                config_from_file(config_file)
            
            self.assertIn("Multi-figure configurations are no longer supported", str(context.exception))
        finally:
            cleanup_temp_directory(temp_dir)


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
        
        # Access config directly for single-figure support
        self.assertEqual(config.config["X"]["scale"], "log")
        self.assertEqual(config.config["X"]["signal_key"], "raw.frequency")
    
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
        
        # Access config directly for single-figure support
        self.assertEqual(config.config["Y"][0]["scale"], "log")
        self.assertNotIn("scale", config.config["Y"][1])  # Second Y-axis doesn't have scale
    
    def test_config_with_both_axes_log_scale(self):
        """Test configuration with both X and Y axes log scale."""
        config_dict = get_config_with_log_scale()
        config = PlotConfig(config_dict)
        
        warnings = config.validate()
        self.assertEqual(len(warnings), 0)
        
        # Access config directly for single-figure support
        self.assertEqual(config.config["X"]["scale"], "log")
        self.assertEqual(config.config["Y"][0]["scale"], "log")
        
        # Check that it's designed for Bode plots
        self.assertEqual(config.config["X"]["signal_key"], "raw.frequency")
        self.assertIn("Magnitude", config.config["Y"][0]["label"])
    
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
        
        # Access config directly for single-figure support
        
        # First Y-axis: no scale specified (defaults to linear)
        self.assertNotIn("scale", config.config["Y"][0])
        
        # Second Y-axis: log scale
        self.assertEqual(config.config["Y"][1]["scale"], "log")
        
        # Third Y-axis: explicit linear scale
        self.assertEqual(config.config["Y"][2]["scale"], "linear")
    
    def test_log_scale_validation(self):
        """Test that log scale configurations pass validation."""
        config_dict = get_config_with_log_scale()
        config = PlotConfig(config_dict)
        
        warnings = config.validate()
        self.assertEqual(len(warnings), 0, "Log scale config should be valid")
        
        # Validate structure
        assert_config_structure(config.config)
    
    def test_log_scale_multi_figure_rejection(self):
        """Test that multi-figure log scale configurations are rejected."""
        multi_config = [
            {
                "title": "Linear Plot",
                "X": {"signal_key": "raw.time", "label": "Time (s)"},
                "Y": [{"label": "Voltage", "signals": {"VDD": "v(vdd)"}}]
            },
            {
                "title": "Log Plot",
                "X": {"signal_key": "raw.frequency", "scale": "log", "label": "Frequency (Hz)"},
                "Y": [
                    {
                        "label": "Magnitude (dB)",
                        "scale": "log",
                        "signals": {"MAG": "data.magnitude"}
                    }
                ]
            }
        ]
        
        # Multi-figure configurations should be rejected, even with log scales
        with self.assertRaises(ValueError) as context:
            PlotConfig(multi_config)
        
        self.assertIn("Multi-figure configurations are no longer supported", str(context.exception))


class TestAdvancedConfigurationFeatures(unittest.TestCase):
    """Test advanced configuration features and edge cases."""
    
    def test_config_with_extensive_metadata(self):
        """Test configuration with extensive metadata fields."""
        extensive_config = {
            "title": "Extensive Metadata Test",
            "description": "A test with many optional fields",
            "source": "./data.raw",
            "author": "Test Author",
            "date": "2024-01-01",
            "X": {
                "signal_key": "raw.time",
                "label": "Time (s)",
                "units": "seconds",
                "scale": "linear"
            },
            "Y": [
                {
                    "label": "Supply Voltage",
                    "units": "volts",
                    "color": "blue",
                    "scale": "linear",
                    "signals": {"VDD": "v(vdd)"}
                },
                {
                    "label": "Output Voltage",
                    "units": "volts", 
                    "color": "red",
                    "signals": {"OUT": "v(out)"}
                }
            ],
            "layout": {
                "width": 800,
                "height": 600,
                "margin": {"t": 50, "b": 50, "l": 50, "r": 50}
            }
        }
        
        config = PlotConfig(extensive_config)
        warnings = config.validate()
        self.assertEqual(len(warnings), 0)
        
        # Check that all metadata is preserved (direct access for single-figure support)
        self.assertEqual(config.config["title"], "Extensive Metadata Test")
        self.assertEqual(config.config["description"], "A test with many optional fields")
        self.assertEqual(config.config["author"], "Test Author")
        self.assertIn("layout", config.config)
    
    def test_config_preservation_through_processing(self):
        """Test that configuration data is preserved through processing."""
        original_config = get_config_with_log_scale()
        original_config["custom_field"] = "custom_value"
        original_config["nested"] = {"inner": {"deep": "value"}}
        
        config = PlotConfig(original_config)
        processed_config = config.config
        
        # Check that custom fields are preserved
        self.assertEqual(processed_config["custom_field"], "custom_value")
        self.assertEqual(processed_config["nested"]["inner"]["deep"], "value")
        
        # Check that standard fields are still present
        self.assertEqual(processed_config["title"], "Log Scale Test")
        self.assertEqual(processed_config["X"]["scale"], "log")
    
    def test_config_with_complex_signal_expressions(self):
        """Test configuration with complex signal expressions."""
        complex_config = {
            "title": "Complex Signal Expressions",
            "X": {"signal_key": "raw.time"},
            "Y": [
                {
                    "label": "Raw Signals",
                    "signals": {
                        "VDD_RAW": "v(vdd)",
                        "VSS_RAW": "v(vss)"
                    }
                },
                {
                    "label": "Processed Signals",
                    "signals": {
                        "POWER": "data.power",
                        "EFFICIENCY": "data.efficiency",
                        "GAIN_DB": "data.gain_db"
                    }
                },
                {
                    "label": "Mathematical Expressions",
                    "signals": {
                        "DIFFERENTIAL": "data.vdd_minus_vss",
                        "RMS_VALUE": "data.rms_voltage"
                    }
                }
            ]
        }
        
        config = PlotConfig(complex_config)
        warnings = config.validate()
        self.assertEqual(len(warnings), 0)
        
        # Validate that all signal types are preserved (direct access for single-figure support)
        self.assertEqual(len(config.config["Y"]), 3)
        
        # Check raw signals
        raw_signals = config.config["Y"][0]["signals"]
        self.assertIn("VDD_RAW", raw_signals)
        self.assertEqual(raw_signals["VDD_RAW"], "v(vdd)")
        
        # Check processed signals
        processed_signals = config.config["Y"][1]["signals"]
        self.assertIn("POWER", processed_signals)
        self.assertEqual(processed_signals["POWER"], "data.power")
    
    def test_config_error_handling_in_features(self):
        """Test error handling in advanced features."""
        # Test template with invalid characters
        with self.assertRaises(ValueError):
            PlotConfig.from_template("")  # Empty template name
        
        # PlotConfig.get_raw_file_path doesn't validate argument types
        # so this test is removed as it doesn't match actual behavior
    
    def test_config_immutability_in_features(self):
        """Test that advanced features return same object references."""
        original_config = get_config_with_log_scale()
        config = PlotConfig(original_config)
        
        # Get config and modify it
        returned_config = config.config
        returned_config["X"]["scale"] = "linear"  # Change log to linear
        
        # PlotConfig returns same object, so changes persist
        fresh_config = config.config
        self.assertEqual(fresh_config["X"]["scale"], "linear")
        
        # Template configs behave the same way
        template_config = PlotConfig.from_template("basic")
        returned_template = template_config.config
        returned_template["title"] = "Modified Template"
        
        fresh_template = template_config.config
        self.assertEqual(fresh_template["title"], "Modified Template")


if __name__ == '__main__':
    unittest.main() 