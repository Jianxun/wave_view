"""
Unit tests for PlotConfig basic functionality.

This module tests core PlotConfig initialization, file path detection,
and basic configuration structure handling.
"""

import unittest
import os
from pathlib import Path
import yaml

from wave_view.core.config import PlotConfig
from wave_view.api import config_from_yaml, config_from_file
from . import (
    create_temp_yaml_file, create_temp_directory_with_config, cleanup_temp_file,
    cleanup_temp_directory, get_basic_config_dict,
    assert_config_structure, get_yaml_test_strings
)


class TestPlotConfigInitialization(unittest.TestCase):
    """Test PlotConfig initialization from various sources."""
    
    def test_init_from_dictionary_single_figure(self):
        """Test creating config from dictionary (single figure)."""
        config_dict = get_basic_config_dict()
        
        config = PlotConfig(config_dict)
        self.assertEqual(config.config["title"], "Basic Test Config")
        self.assertEqual(config.config["X"]["signal_key"], "raw.time")
        self.assertEqual(len(config.config["Y"]), 2)
        
        # Validate structure using shared utility
        assert_config_structure(config.config)
    
    def test_init_from_list_multi_figure_rejected(self):
        """Test that list inputs (multi-figure configs) are rejected."""
        config_list = [
            {"title": "Figure 1", "X": {"signal_key": "time"}, "Y": []},
            {"title": "Figure 2", "X": {"signal_key": "time"}, "Y": []}
        ]
        
        with self.assertRaises(ValueError) as context:
            PlotConfig(config_list)
        
        self.assertIn("Multi-figure configurations are no longer supported", str(context.exception))
    
    def test_init_from_yaml_string(self):
        """Test creating config from YAML string content using config_from_yaml."""
        yaml_strings = get_yaml_test_strings()
        yaml_content = yaml_strings["multiline_yaml"]
        
        config = config_from_yaml(yaml_content)
        self.assertEqual(config.config["title"], "Multi-line Test")
        self.assertEqual(config.config["X"]["signal_key"], "raw.time")
        self.assertEqual(config.config["X"]["label"], "Time (s)")
        
        # Check Y configuration
        self.assertEqual(len(config.config["Y"]), 1)
        self.assertEqual(config.config["Y"][0]["label"], "Voltage")
        self.assertEqual(config.config["Y"][0]["signals"]["VDD"], "v(vdd)")
    
    def test_init_from_yaml_list_string_rejected(self):
        """Test that YAML list strings (multi-figure configs) are rejected."""
        yaml_strings = get_yaml_test_strings()
        yaml_content = yaml_strings["list_yaml"]
        
        with self.assertRaises(ValueError) as context:
            config_from_yaml(yaml_content)
        
        self.assertIn("Multi-figure configurations are no longer supported", str(context.exception))
    
    def test_init_invalid_type(self):
        """Test initialization with invalid input types."""
        invalid_inputs = [
            (12345, "integer"),
            (None, "None"),
            (3.14, "float"),
            (set(), "set"),
            (lambda x: x, "function"),
            ("yaml string", "string")  # Strings no longer accepted directly
        ]
        
        for invalid_input, input_type in invalid_inputs:
            with self.subTest(input_type=input_type):
                with self.assertRaises(ValueError) as context:
                    PlotConfig(invalid_input)
                
                self.assertIn("Config source must be Path or dict", str(context.exception))
    
    def test_init_empty_inputs(self):
        """Test initialization with empty but valid inputs."""
        # Empty dict - should be accepted
        config = PlotConfig({})
        self.assertEqual(config.config, {})
        
        # Empty list - should be rejected 
        with self.assertRaises(ValueError) as context:
            PlotConfig([])
        
        self.assertIn("Multi-figure configurations are no longer supported", str(context.exception))


class TestFileBasedInitialization(unittest.TestCase):
    """Test PlotConfig initialization from files and Path objects."""
    
    def test_init_from_yaml_file(self):
        """Test creating config from YAML file using config_from_file."""
        config_dict = get_basic_config_dict()
        temp_path = create_temp_yaml_file(config_dict)
        
        try:
            config = config_from_file(temp_path)
            self.assertEqual(config.config["title"], "Basic Test Config")
            self.assertEqual(config.config["X"]["signal_key"], "raw.time")
            
            # Verify Y configuration
            self.assertEqual(len(config.config["Y"]), 2)
            self.assertEqual(config.config["Y"][0]["label"], "Voltage")
            self.assertEqual(config.config["Y"][1]["label"], "Current")
        finally:
            cleanup_temp_file(temp_path)
    
    def test_init_from_path_object(self):
        """Test creating config from Path object."""
        config_dict = get_basic_config_dict()
        config_dict["title"] = "Path Object Test"
        
        temp_path_str = create_temp_yaml_file(config_dict)
        temp_path = Path(temp_path_str)
        
        try:
            config = PlotConfig(temp_path)
            self.assertEqual(config.config["title"], "Path Object Test")
            assert_config_structure(config.config)
        finally:
            cleanup_temp_file(temp_path_str)
    
    def test_init_from_yaml_file_multi_figure_rejected(self):
        """Test that YAML files with lists (multi-figure configs) are rejected."""
        config_list = [
            {"title": "Figure 1", "X": {"signal_key": "time"}, "Y": []},
            {"title": "Figure 2", "X": {"signal_key": "time"}, "Y": []}
        ]
        temp_path = create_temp_yaml_file(config_list)
        
        try:
            with self.assertRaises(ValueError) as context:
                config_from_file(temp_path)
            
            self.assertIn("Multi-figure configurations are no longer supported", str(context.exception))
        finally:
            cleanup_temp_file(temp_path)
    
    def test_init_nonexistent_file(self):
        """Test initialization with non-existent file using config_from_file."""
        with self.assertRaises(FileNotFoundError) as context:
            config_from_file("nonexistent_config.yaml")
        
        self.assertIn("Configuration file not found", str(context.exception))
        self.assertIn("nonexistent_config.yaml", str(context.exception))
    
    def test_init_invalid_yaml_file(self):
        """Test initialization with invalid YAML file using config_from_file."""
        invalid_yaml = """
        title: "Invalid YAML
        X: {
          signal_key: "raw.time"
          # Missing closing brace and quote
        """
        
        temp_path = create_temp_yaml_file(invalid_yaml)
        
        try:
            with self.assertRaises(yaml.YAMLError) as context:
                config_from_file(temp_path)
            
            self.assertIn("Invalid YAML in config file", str(context.exception))
        finally:
            cleanup_temp_file(temp_path)
    
    def test_init_invalid_yaml_string(self):
        """Test initialization with invalid YAML string content using config_from_yaml."""
        invalid_yaml_string = """
        title: "Invalid YAML String
        X: {
          signal_key: "raw.time"
          # Missing closing brace and quote
        """
        
        with self.assertRaises(yaml.YAMLError) as context:
            config_from_yaml(invalid_yaml_string)
        
        self.assertIn("Invalid YAML content", str(context.exception))
    
    def test_init_yaml_file_different_extensions(self):
        """Test YAML file loading with different extensions using config_from_file."""
        config_dict = get_basic_config_dict()
        extensions = ['.yaml', '.yml', '.json']  # json should also work
        
        for ext in extensions:
            with self.subTest(extension=ext):
                temp_path = create_temp_yaml_file(config_dict, suffix=ext)
                try:
                    config = config_from_file(temp_path)
                    self.assertEqual(config.config["title"], "Basic Test Config")
                finally:
                    cleanup_temp_file(temp_path)


class TestConfigurationStructureAccess(unittest.TestCase):
    """Test configuration structure access and properties."""
    
    def test_single_figure_properties(self):
        """Test properties for single figure configuration."""
        config_dict = get_basic_config_dict()
        config = PlotConfig(config_dict)
        
        # Test basic config access
        self.assertEqual(config.config["title"], "Basic Test Config")
        self.assertEqual(len(config.config["Y"]), 2)
        self.assertEqual(config.config["X"]["signal_key"], "raw.time")
    

    
    def test_config_property_access(self):
        """Test accessing configuration properties."""
        config_dict = get_basic_config_dict()
        config = PlotConfig(config_dict)
        
        # Test config property
        raw_config = config.config
        self.assertEqual(raw_config["title"], "Basic Test Config")
        self.assertIsInstance(raw_config, dict)
        
        # Test to_dict method
        dict_config = config.to_dict()
        self.assertEqual(dict_config["title"], "Basic Test Config")
        self.assertEqual(dict_config, raw_config)
    
    def test_config_immutability(self):
        """Test that returned configs are references (not deep copies)."""
        config_dict = get_basic_config_dict()
        config = PlotConfig(config_dict)
        
        # Get config and modify it
        returned_config = config.config
        returned_config["title"] = "Modified Title"
        
        # PlotConfig returns the same object reference, so changes persist
        fresh_config = config.config
        self.assertEqual(fresh_config["title"], "Modified Title")
        self.assertIs(fresh_config, returned_config)  # Same object reference
    
    def test_string_representation(self):
        """Test __repr__ method for configurations."""
        # Single figure
        single_config = PlotConfig(get_basic_config_dict())
        repr_str = repr(single_config)
        self.assertIn("PlotConfig", repr_str)
        self.assertIn("Basic Test Config", repr_str)


class TestInvalidConfigurationStructures(unittest.TestCase):
    """Test handling of invalid configuration structures."""
    
    def test_invalid_configuration_types(self):
        """Test that lists are rejected as multi-figure configs are no longer supported."""
        # Any list should be rejected
        invalid_configs = [
            [get_basic_config_dict()],  # Single-item list
            [get_basic_config_dict(), get_basic_config_dict()],  # Multi-item list
            [],  # Empty list
            ["string"],  # List with string
            [None],  # List with None
        ]
        
        for i, invalid_config in enumerate(invalid_configs):
            with self.subTest(config_index=i):
                with self.assertRaises(ValueError) as context:
                    PlotConfig(invalid_config)
                
                self.assertIn("Multi-figure configurations are no longer supported", str(context.exception))


if __name__ == '__main__':
    unittest.main() 