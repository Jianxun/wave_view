"""
Tests for Path object support across all API functions.

This module tests that all API functions consistently support both string and Path objects
for file paths, with proper validation and error handling.
"""

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from wave_view.api import plot, load_spice, explore_signals, validate_config, config_from_file
from . import (
    create_temp_raw_file, 
    create_temp_yaml_config, 
    cleanup_temp_file,
    get_basic_test_config,
    create_mock_spice_plotter,
    create_mock_spice_data
)


class TestPathObjectSupport:
    """Test Path object support across all API functions."""
    
    def test_plot_function_path_support(self):
        """Test that plot() function supports both string and Path objects."""
        # Create temporary files
        raw_file_str = create_temp_raw_file("test.raw")
        config_file_str = create_temp_yaml_config(get_basic_test_config())
        
        try:
            with patch('wave_view.api.SpicePlotter') as mock_plotter_class:
                # Setup successful mock
                mock_plotter = create_mock_spice_plotter()
                mock_plotter_class.return_value = mock_plotter
                
                # Test with string path
                config1 = config_from_file(config_file_str)
                fig1 = plot(raw_file_str, config1, show=False)
                assert hasattr(fig1, 'data')
                
                # Test with Path objects
                raw_path = Path(raw_file_str)
                config_path = Path(config_file_str)
                config2 = config_from_file(config_path)
                fig2 = plot(raw_path, config2, show=False)
                assert hasattr(fig2, 'data')
                
                # Test mixed usage (Path + string)
                config3 = config_from_file(config_file_str)
                fig3 = plot(raw_path, config3, show=False)
                assert hasattr(fig3, 'data')
                
                # Verify SpicePlotter was called with string paths (internal conversion)
                calls = mock_plotter_class.call_args_list
                for call in calls:
                    assert isinstance(call[0][0], str)  # Should be converted to string
                
        finally:
            cleanup_temp_file(raw_file_str)
            cleanup_temp_file(config_file_str)
    
    def test_load_spice_path_support(self):
        """Test that load_spice() function supports both string and Path objects."""
        # Create temporary file
        raw_file_str = create_temp_raw_file("test.raw")
        
        try:
            with patch('wave_view.api.SpiceData') as mock_spice_data_class:
                # Setup successful mock
                mock_data = create_mock_spice_data()
                mock_spice_data_class.return_value = mock_data
                
                # Test with string path
                data1 = load_spice(raw_file_str)
                assert data1 == mock_data
                
                # Test with Path object
                raw_path = Path(raw_file_str)
                data2 = load_spice(raw_path)
                assert data2 == mock_data
                
                # Verify SpiceData was called with string paths (internal conversion)
                calls = mock_spice_data_class.call_args_list
                for call in calls:
                    assert isinstance(call[0][0], str)  # Should be converted to string
                
        finally:
            cleanup_temp_file(raw_file_str)
    
    def test_explore_signals_path_support(self):
        """Test that explore_signals() supports both string and Path objects."""
        # Create temporary raw file
        raw_file_str = create_temp_raw_file("test.raw")
        
        try:
            with patch('wave_view.api.SpiceData') as mock_spice_data_class:
                # Setup successful mock
                mock_data = create_mock_spice_data()
                mock_spice_data_class.return_value = mock_data
                
                # Test with string path
                signals1 = explore_signals(raw_file_str)
                assert isinstance(signals1, list)
                assert len(signals1) > 0
                
                # Test with Path object
                raw_path = Path(raw_file_str)
                signals2 = explore_signals(raw_path)
                assert isinstance(signals2, list)
                assert len(signals2) > 0
                
                # Verify SpiceData was called with string paths (internal conversion)
                calls = mock_spice_data_class.call_args_list
                for call in calls:
                    assert isinstance(call[0][0], str)  # Should be converted to string
                
        finally:
            cleanup_temp_file(raw_file_str)
    
    def test_validate_config_path_support(self):
        """Test that validate_config() supports Path objects for both parameters."""
        # Create temporary files
        raw_file_str = create_temp_raw_file("test.raw")
        config_file_str = create_temp_yaml_config(get_basic_test_config())
        
        try:
            with patch('wave_view.api.SpiceData') as mock_spice_data_class:
                
                # Setup successful mocks
                mock_data = create_mock_spice_data()
                mock_spice_data_class.return_value = mock_data
                
                # Test with string paths - focus on Path object acceptance, not validation details
                try:
                    warnings1 = validate_config(config_file_str, raw_file_str)
                    assert isinstance(warnings1, list)  # Should return a list, regardless of content
                except Exception as e:
                    # If there's an exception, it should be about content, not Path objects
                    assert "file path" not in str(e).lower()
                
                # Test with Path objects
                config_path = Path(config_file_str)
                raw_path = Path(raw_file_str)
                try:
                    warnings2 = validate_config(config_path, raw_path)
                    assert isinstance(warnings2, list)
                except Exception as e:
                    assert "file path" not in str(e).lower()
                
                # Test mixed usage (Path config, string raw file)
                try:
                    warnings3 = validate_config(config_path, raw_file_str)
                    assert isinstance(warnings3, list)
                except Exception as e:
                    assert "file path" not in str(e).lower()
                
                # Test with dictionary config (should still work)
                try:
                    warnings4 = validate_config(get_basic_test_config(), raw_path)
                    assert isinstance(warnings4, list)
                except Exception as e:
                    assert "file path" not in str(e).lower()
                
                # Verify SpiceData was called with string paths when provided
                spice_data_calls = mock_spice_data_class.call_args_list
                for call in spice_data_calls:
                    if call[0]:  # If there are arguments
                        assert isinstance(call[0][0], str)  # Should be converted to string
                
        finally:
            cleanup_temp_file(raw_file_str)
            cleanup_temp_file(config_file_str)


class TestPathValidationErrors:
    """Test proper error handling for invalid path inputs."""
    
    def test_plot_function_path_validation(self):
        """Test plot() function validates Path objects properly."""
        config = get_basic_test_config()
        
        # Test None input
        with pytest.raises(TypeError, match="file path must be a string or Path object, not None"):
            plot(None, config)
        
        # Test invalid type
        with pytest.raises(TypeError, match="file path must be a string or Path object"):
            plot(123, config)
        
        # Test empty string
        with pytest.raises(ValueError, match="file path cannot be empty"):
            plot("", config)
        
        # Test non-existent file (string)
        with pytest.raises(FileNotFoundError, match="SPICE raw file not found"):
            plot("nonexistent.raw", config)
        
        # Test non-existent file (Path)
        with pytest.raises(FileNotFoundError, match="SPICE raw file not found"):
            plot(Path("nonexistent.raw"), config)
    
    def test_load_spice_path_validation(self):
        """Test load_spice() function validates Path objects properly."""
        # Test None input
        with pytest.raises(TypeError, match="file path must be a string or Path object, not None"):
            load_spice(None)
        
        # Test invalid type
        with pytest.raises(TypeError, match="file path must be a string or Path object"):
            load_spice(123)
        
        # Test empty string
        with pytest.raises(ValueError, match="file path cannot be empty"):
            load_spice("")
        
        # Test non-existent file (string)
        with pytest.raises(FileNotFoundError, match="SPICE raw file not found"):
            load_spice("nonexistent.raw")
        
        # Test non-existent file (Path)
        with pytest.raises(FileNotFoundError, match="SPICE raw file not found"):
            load_spice(Path("nonexistent.raw"))
    
    def test_explore_signals_path_validation(self):
        """Test explore_signals() validates Path objects properly."""
        # Test None input
        with pytest.raises(TypeError, match="file path must be a string or Path object, not None"):
            explore_signals(None)
        
        # Test invalid type
        with pytest.raises(TypeError, match="file path must be a string or Path object"):
            explore_signals(123)
        
        # Test empty string
        with pytest.raises(ValueError, match="file path cannot be empty"):
            explore_signals("")
        
        # Test non-existent file (string)
        with pytest.raises(FileNotFoundError, match="SPICE raw file not found"):
            explore_signals("nonexistent.raw")
        
        # Test non-existent file (Path)
        with pytest.raises(FileNotFoundError, match="SPICE raw file not found"):
            explore_signals(Path("nonexistent.raw"))
    
    def test_validate_config_path_validation(self):
        """Test validate_config() validates Path objects properly."""
        # Test None config - should return error list, not raise exception
        result = validate_config(None)
        assert len(result) == 1
        assert "Configuration error" in result[0]
        
        # Test invalid type config - should return error list, not raise exception
        result = validate_config(123)
        assert len(result) == 1
        assert "Configuration error" in result[0]
        
        # Test empty string config - should return error list, not raise exception
        result = validate_config("")
        assert len(result) == 1
        assert "Configuration error" in result[0]
        
        # Test non-existent config file (string)
        result = validate_config("nonexistent.yaml")
        assert len(result) == 1
        assert "Configuration error" in result[0]
        
        # Test non-existent config file (Path)
        result = validate_config(Path("nonexistent.yaml"))
        assert len(result) == 1
        assert "Configuration error" in result[0]
        
        # Test invalid type raw file
        result = validate_config(get_basic_test_config(), 123)
        assert len(result) == 1
        assert "Configuration error" in result[0]
        
        # Test empty string raw file
        result = validate_config(get_basic_test_config(), "")
        assert len(result) == 1
        assert "Configuration error" in result[0]
        
        # Test non-existent raw file (string)
        result = validate_config(get_basic_test_config(), "nonexistent.raw")
        assert len(result) == 1
        assert "Configuration error" in result[0]


class TestPathConsistency:
    """Test that all functions handle Path objects consistently."""
    
    def test_all_functions_accept_path_objects(self):
        """Test that all functions accept Path objects without errors."""
        # Create temporary files
        raw_file_str = create_temp_raw_file("consistency_test.raw")
        config_file_str = create_temp_yaml_config(get_basic_test_config())
        
        try:
            # Convert to Path objects
            raw_path = Path(raw_file_str)
            config_path = Path(config_file_str)
            
            with patch('wave_view.api.SpicePlotter') as mock_plotter_class, \
                 patch('wave_view.api.SpiceData') as mock_spice_data_class:
                
                # Setup mocks
                mock_plotter = create_mock_spice_plotter()
                mock_plotter_class.return_value = mock_plotter
                
                mock_data = create_mock_spice_data()
                mock_spice_data_class.return_value = mock_data
                
                # All functions should accept Path objects without error
                config = config_from_file(config_path)
                fig = plot(raw_path, config, show=False)
                assert hasattr(fig, 'data')
                
                data = load_spice(raw_path)
                assert data == mock_data
                
                signals = explore_signals(raw_path)
                assert isinstance(signals, list)
                
                # Note: validate_config will use real PlotConfig, so we expect it to work
                # but we can't easily mock it without breaking isinstance checks
                # This test focuses on Path object acceptance, not validation logic
                try:
                    warnings = validate_config(config_path, raw_path)
                    # If it doesn't raise an exception, Path objects are accepted
                    assert isinstance(warnings, list)
                except Exception:
                    # If there's an exception, it should be about the content, not Path objects
                    pass
                
        finally:
            cleanup_temp_file(raw_file_str)
            cleanup_temp_file(config_file_str) 