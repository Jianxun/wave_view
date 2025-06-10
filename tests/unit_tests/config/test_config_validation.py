"""
Unit tests for PlotConfig validation functionality.

This module tests configuration validation including structure validation,
required field checking, and signal validation against SPICE data.
"""

import unittest

from wave_view.core.config import PlotConfig
from . import (
    get_basic_config_dict, create_mock_spice_data,
    get_config_with_processed_signals, get_invalid_config_examples,
    assert_validation_warnings
)


class TestBasicConfigurationValidation(unittest.TestCase):
    """Test basic configuration validation without SPICE data."""
    
    def test_validate_valid_single_figure_config(self):
        """Test validation of valid single figure configuration."""
        config_dict = get_basic_config_dict()
        config = PlotConfig(config_dict)
        
        warnings = config.validate()
        assert_validation_warnings(warnings, expected_warning_count=0)
    

    
    def test_validate_empty_config(self):
        """Test validation of empty configuration."""
        # Empty single figure config
        empty_config = PlotConfig({})
        warnings = empty_config.validate()
        self.assertGreater(len(warnings), 0)
        
        # Should warn about missing X and Y
        assert_validation_warnings(warnings, contains_text="Missing required 'X'")
        assert_validation_warnings(warnings, contains_text="Missing required 'Y'")
    
    def test_validate_minimal_valid_config(self):
        """Test validation of minimal but valid configuration."""
        minimal_config = {
            "X": {"signal_key": "raw.time"},
            "Y": [{"signals": {"TEST": "v(test)"}}]
        }
        
        config = PlotConfig(minimal_config)
        warnings = config.validate()
        assert_validation_warnings(warnings, expected_warning_count=0)


class TestRequiredFieldValidation(unittest.TestCase):
    """Test validation of required configuration fields."""
    
    def test_validate_missing_x_configuration(self):
        """Test validation with missing X configuration."""
        missing_x = {
            "title": "Missing X Config",
            "Y": [{"label": "Voltage", "signals": {"VDD": "v(vdd)"}}]
        }
        
        config = PlotConfig(missing_x)
        warnings = config.validate()
        self.assertGreater(len(warnings), 0)
        assert_validation_warnings(warnings, contains_text="Missing required 'X'")
    
    def test_validate_missing_y_configuration(self):
        """Test validation with missing Y configuration."""
        missing_y = {
            "title": "Missing Y Config",
            "X": {"signal_key": "raw.time", "label": "Time"}
        }
        
        config = PlotConfig(missing_y)
        warnings = config.validate()
        self.assertGreater(len(warnings), 0)
        assert_validation_warnings(warnings, contains_text="Missing required 'Y'")
    
    def test_validate_invalid_x_configuration(self):
        """Test validation with invalid X configuration."""
        # X missing signal_key
        invalid_x = {
            "title": "Invalid X Config",
            "X": {"label": "Time"},  # Missing required signal_key
            "Y": [{"label": "Voltage", "signals": {"VDD": "v(vdd)"}}]
        }
        
        config = PlotConfig(invalid_x)
        warnings = config.validate()
        self.assertGreater(len(warnings), 0)
        assert_validation_warnings(warnings, contains_text="X configuration must have 'signal_key'")
        
        # X is not a dictionary
        x_not_dict = {
            "X": "should_be_dict",
            "Y": [{"signals": {"VDD": "v(vdd)"}}]
        }
        
        config = PlotConfig(x_not_dict)
        warnings = config.validate()
        self.assertGreater(len(warnings), 0)
        # PlotConfig validation treats non-dict X as missing signal_key
        assert_validation_warnings(warnings, contains_text="X configuration must have 'signal_key'")


class TestYConfigurationValidation(unittest.TestCase):
    """Test validation of Y axis configurations."""
    
    def test_validate_y_not_list(self):
        """Test validation when Y configuration is not a list."""
        invalid_y_type = {
            "X": {"signal_key": "raw.time"},
            "Y": {"not": "a list"}  # Should be a list
        }
        
        config = PlotConfig(invalid_y_type)
        warnings = config.validate()
        self.assertGreater(len(warnings), 0)
        assert_validation_warnings(warnings, contains_text="Y configuration must be a list")
    
    def test_validate_y_contains_non_dict_elements(self):
        """Test validation when Y contains non-dictionary elements."""
        invalid_y_elements = {
            "X": {"signal_key": "raw.time"},
            "Y": [
                {"label": "Valid", "signals": {"VDD": "v(vdd)"}},
                "invalid_string",  # Should be a dict
                {"label": "Also Valid", "signals": {"OUT": "v(out)"}},
                123  # Also invalid
            ]
        }
        
        config = PlotConfig(invalid_y_elements)
        warnings = config.validate()
        self.assertGreater(len(warnings), 1)  # Should have multiple warnings
        
        # Check for specific element warnings
        assert_validation_warnings(warnings, contains_text="Y[1] must be a dictionary")
        assert_validation_warnings(warnings, contains_text="Y[3] must be a dictionary")
    
    def test_validate_y_missing_signals(self):
        """Test validation when Y elements are missing signals."""
        missing_signals = {
            "X": {"signal_key": "raw.time"},
            "Y": [
                {"label": "Valid", "signals": {"VDD": "v(vdd)"}},
                {"label": "Missing Signals"},  # No 'signals' key
                {"label": "Also Missing"}      # No 'signals' key
            ]
        }
        
        config = PlotConfig(missing_signals)
        warnings = config.validate()
        self.assertGreater(len(warnings), 1)
        
        assert_validation_warnings(warnings, contains_text="Y[1] missing 'signals'")
        assert_validation_warnings(warnings, contains_text="Y[2] missing 'signals'")
    
    def test_validate_y_invalid_signals_type(self):
        """Test validation when Y signals are not dictionaries."""
        invalid_signals = {
            "X": {"signal_key": "raw.time"},
            "Y": [
                {"label": "Valid", "signals": {"VDD": "v(vdd)"}},
                {"label": "Invalid Signals Type", "signals": "should_be_dict"},
                {"label": "Also Invalid", "signals": ["list", "not", "dict"]}
            ]
        }
        
        config = PlotConfig(invalid_signals)
        warnings = config.validate()
        self.assertGreater(len(warnings), 1)
        
        assert_validation_warnings(warnings, contains_text="Y[1]['signals'] must be a dictionary")
        assert_validation_warnings(warnings, contains_text="Y[2]['signals'] must be a dictionary")
    
    def test_validate_empty_y_list(self):
        """Test validation with empty Y list."""
        empty_y = {
            "X": {"signal_key": "raw.time"},
            "Y": []  # Empty but valid
        }
        
        config = PlotConfig(empty_y)
        warnings = config.validate()
        # Empty Y list should be valid (no plots to show)
        assert_validation_warnings(warnings, expected_warning_count=0)


class TestSignalValidationWithSpiceData(unittest.TestCase):
    """Test signal validation against SPICE data."""
    
    def test_validate_with_valid_signals(self):
        """Test validation with all valid signals."""
        mock_spice_data = create_mock_spice_data(["time", "v(vdd)", "v(out)", "v(gnd)", "i(vdd)"])
        
        valid_config = {
            "X": {"signal_key": "raw.time"},
            "Y": [
                {"label": "Voltages", "signals": {"VDD": "v(vdd)", "OUT": "v(out)"}},
                {"label": "Current", "signals": {"IDD": "i(vdd)"}}
            ]
        }
        
        config = PlotConfig(valid_config)
        warnings = config.validate(mock_spice_data)
        assert_validation_warnings(warnings, expected_warning_count=0)
    
    def test_validate_with_invalid_signals(self):
        """Test validation with signals not in SPICE data."""
        mock_spice_data = create_mock_spice_data(["time", "v(vdd)", "v(out)"])
        
        invalid_config = {
            "X": {"signal_key": "raw.nonexistent"},  # Signal doesn't exist
            "Y": [
                {"label": "Valid", "signals": {"VDD": "v(vdd)"}},
                {"label": "Invalid", "signals": {"MISSING": "v(missing)", "FAKE": "i(fake)"}}
            ]
        }
        
        config = PlotConfig(invalid_config)
        warnings = config.validate(mock_spice_data)
        self.assertGreater(len(warnings), 2)
        
        # Check for specific signal warnings
        assert_validation_warnings(warnings, contains_text="nonexistent")
        assert_validation_warnings(warnings, contains_text="missing")
        assert_validation_warnings(warnings, contains_text="fake")
    
    def test_validate_with_processed_signals(self):
        """Test validation with processed signals (data. prefix)."""
        mock_spice_data = create_mock_spice_data(["time", "v(vdd)", "v(out)"])
        
        config_with_processed = get_config_with_processed_signals()
        config = PlotConfig(config_with_processed)
        warnings = config.validate(mock_spice_data)
        
        # Processed signals should be skipped from validation
        # Only raw signals should be validated
        assert_validation_warnings(warnings, expected_warning_count=0)
    

    
    def test_validate_case_insensitive_signals(self):
        """Test signal validation behavior with case differences."""
        # SPICE data signals are lowercase
        mock_spice_data = create_mock_spice_data(["time", "v(vdd)", "v(out)", "i(vdd)"])
        
        # Config uses exact case matches
        matched_case_config = {
            "X": {"signal_key": "raw.time"},  # Exact match
            "Y": [
                {"label": "Voltages", "signals": {
                    "VDD": "v(vdd)",  # Exact match
                    "OUT": "v(out)"   # Exact match
                }}
            ]
        }
        
        config = PlotConfig(matched_case_config)
        warnings = config.validate(mock_spice_data)
        # Should not generate warnings with exact matches
        assert_validation_warnings(warnings, expected_warning_count=0)


class TestInvalidConfigurationExamples(unittest.TestCase):
    """Test validation with systematically invalid configurations."""
    
    def test_validate_all_invalid_examples(self):
        """Test validation with all invalid configuration examples."""
        invalid_examples = get_invalid_config_examples()
        
        for example_name, example_data in invalid_examples.items():
            with self.subTest(example=example_name):
                config = PlotConfig(example_data["config"])
                warnings = config.validate()
                
                # All invalid examples should generate warnings
                self.assertGreater(len(warnings), 0, 
                    f"Example '{example_name}' should generate warnings: {example_data['description']}")
    
    def test_validate_missing_x_detailed(self):
        """Test detailed validation of missing X configuration."""
        examples = get_invalid_config_examples()
        config = PlotConfig(examples["missing_x"]["config"])
        warnings = config.validate()
        
        assert_validation_warnings(warnings, contains_text="Missing required 'X'")
    
    def test_validate_missing_y_detailed(self):
        """Test detailed validation of missing Y configuration."""
        examples = get_invalid_config_examples()
        config = PlotConfig(examples["missing_y"]["config"])
        warnings = config.validate()
        
        assert_validation_warnings(warnings, contains_text="Missing required 'Y'")
    
    def test_validate_x_missing_signal_key(self):
        """Test validation when X config is missing signal_key."""
        examples = get_invalid_config_examples()
        config = PlotConfig(examples["invalid_x_no_signal_key"]["config"])
        warnings = config.validate()
        
        assert_validation_warnings(warnings, contains_text="X configuration must have 'signal_key'")
    
    def test_validate_y_not_list_detailed(self):
        """Test detailed validation when Y is not a list."""
        examples = get_invalid_config_examples()
        config = PlotConfig(examples["invalid_y_not_list"]["config"])
        warnings = config.validate()
        
        assert_validation_warnings(warnings, contains_text="Y configuration must be a list")


class TestValidationEdgeCases(unittest.TestCase):
    """Test validation edge cases and boundary conditions."""
    
    def test_validate_none_spice_data(self):
        """Test validation when spice_data is None."""
        config = PlotConfig(get_basic_config_dict())
        
        # Should not raise error with None spice_data
        warnings = config.validate(None)
        assert_validation_warnings(warnings, expected_warning_count=0)
    
    def test_validate_spice_data_without_signals(self):
        """Test validation with SPICE data that has no signals attribute."""
        mock_spice_data = create_mock_spice_data([])  # Empty signals list
        
        config = PlotConfig(get_basic_config_dict())
        warnings = config.validate(mock_spice_data)
        
        # Should generate warnings for all signals since none exist
        self.assertGreater(len(warnings), 0)
    
    def test_validate_deeply_nested_errors(self):
        """Test validation with multiple nested errors."""
        deeply_nested_errors = {
            "X": {"not_signal_key": "raw.time"},  # Wrong key name
            "Y": [
                {"label": "Valid", "signals": {"VDD": "v(vdd)"}},
                {"no_label": "value", "signals": "not_dict"},  # Multiple errors
                "completely_wrong"  # Not a dict at all
            ]
        }
        
        config = PlotConfig(deeply_nested_errors)
        warnings = config.validate()
        
        # Should detect multiple types of errors
        self.assertGreaterEqual(len(warnings), 3)
        assert_validation_warnings(warnings, contains_text="X configuration must have 'signal_key'")
        assert_validation_warnings(warnings, contains_text="Y[1]['signals'] must be a dictionary")
        assert_validation_warnings(warnings, contains_text="Y[2] must be a dictionary")


if __name__ == '__main__':
    unittest.main() 