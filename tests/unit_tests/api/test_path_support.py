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

from wave_view.api import plot, load_spice, create_config_template, validate_config
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
                fig1 = plot(raw_file_str, config_file_str, show=False)
                assert hasattr(fig1, 'data')
                
                # Test with Path objects
                raw_path = Path(raw_file_str)
                config_path = Path(config_file_str)
                fig2 = plot(raw_path, config_path, show=False)
                assert hasattr(fig2, 'data')
                
                # Test mixed usage (Path + string)
                fig3 = plot(raw_path, config_file_str, show=False)
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
    
    def test_create_config_template_path_support(self):
        """Test that create_config_template() supports Path objects for both parameters."""
        # Create temporary raw file
        raw_file_str = create_temp_raw_file("test.raw")
        
        try:
            with patch('wave_view.api.SpiceData') as mock_spice_data_class:
                # Setup successful mock
                mock_data = create_mock_spice_data()
                mock_spice_data_class.return_value = mock_data
                
                # Test with string paths
                output_path1 = "test_config1.yaml"
                create_config_template(output_path1, raw_file_str)
                assert Path(output_path1).exists()
                cleanup_temp_file(output_path1)
                
                # Test with Path objects
                output_path2 = Path("test_config2.yaml")
                raw_path = Path(raw_file_str)
                create_config_template(output_path2, raw_path)
                assert output_path2.exists()
                cleanup_temp_file(str(output_path2))
                
                # Test mixed usage (Path output, string raw file)
                output_path3 = Path("test_config3.yaml")
                create_config_template(output_path3, raw_file_str)
                assert output_path3.exists()
                cleanup_temp_file(str(output_path3))
                
                # Test without raw file (only output path as Path)
                output_path4 = Path("test_config4.yaml")
                create_config_template(output_path4)
                assert output_path4.exists()
                cleanup_temp_file(str(output_path4))
                
        finally:
            cleanup_temp_file(raw_file_str)
    
    def test_validate_config_path_support(self):
        """Test that validate_config() supports Path objects for both parameters."""
        # Create temporary files
        raw_file_str = create_temp_raw_file("test.raw")
        config_file_str = create_temp_yaml_config(get_basic_test_config())
        
        try:
            with patch('wave_view.api.PlotConfig') as mock_config_class, \
                 patch('wave_view.api.SpiceData') as mock_spice_data_class:
                
                # Setup successful mocks
                mock_config = Mock()
                mock_config.validate.return_value = []  # No warnings
                mock_config_class.return_value = mock_config
                
                mock_data = create_mock_spice_data()
                mock_spice_data_class.return_value = mock_data
                
                # Test with string paths
                warnings1 = validate_config(config_file_str, raw_file_str)
                assert warnings1 == []
                
                # Test with Path objects
                config_path = Path(config_file_str)
                raw_path = Path(raw_file_str)
                warnings2 = validate_config(config_path, raw_path)
                assert warnings2 == []
                
                # Test mixed usage (Path config, string raw file)
                warnings3 = validate_config(config_path, raw_file_str)
                assert warnings3 == []
                
                # Test with dictionary config (should still work)
                warnings4 = validate_config(get_basic_test_config(), raw_path)
                assert warnings4 == []
                
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
        # Test None input
        with pytest.raises(TypeError, match="file path must be a string or Path object, not None"):
            plot(None)
        
        # Test invalid type
        with pytest.raises(TypeError, match="file path must be a string or Path object"):
            plot(123)
        
        # Test empty string
        with pytest.raises(ValueError, match="file path cannot be empty"):
            plot("")
        
        # Test non-existent file (string)
        with pytest.raises(FileNotFoundError, match="SPICE raw file not found"):
            plot("nonexistent.raw")
        
        # Test non-existent file (Path)
        with pytest.raises(FileNotFoundError, match="SPICE raw file not found"):
            plot(Path("nonexistent.raw"))
    
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
    
    def test_create_config_template_path_validation(self):
        """Test create_config_template() validates Path objects properly."""
        # Test None output path
        with pytest.raises(TypeError, match="output path must be a string or Path object, not None"):
            create_config_template(None)
        
        # Test invalid type output path
        with pytest.raises(TypeError, match="output path must be a string or Path object"):
            create_config_template(123)
        
        # Test empty string output path
        with pytest.raises(ValueError, match="output path cannot be empty"):
            create_config_template("")
        
        # Test invalid type raw file
        with pytest.raises(TypeError, match="raw file path must be a string or Path object"):
            create_config_template("output.yaml", 123)
        
        # Test empty string raw file
        with pytest.raises(ValueError, match="raw file path cannot be empty"):
            create_config_template("output.yaml", "")
        
        # Test non-existent raw file (string)
        with pytest.raises(FileNotFoundError, match="SPICE raw file not found"):
            create_config_template("output.yaml", "nonexistent.raw")
        
        # Test non-existent raw file (Path)
        with pytest.raises(FileNotFoundError, match="SPICE raw file not found"):
            create_config_template("output.yaml", Path("nonexistent.raw"))
    
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
                 patch('wave_view.api.SpiceData') as mock_spice_data_class, \
                 patch('wave_view.api.PlotConfig') as mock_config_class:
                
                # Setup mocks
                mock_plotter = create_mock_spice_plotter()
                mock_plotter_class.return_value = mock_plotter
                
                mock_data = create_mock_spice_data()
                mock_spice_data_class.return_value = mock_data
                
                mock_config = Mock()
                mock_config.validate.return_value = []
                mock_config_class.return_value = mock_config
                
                # All functions should accept Path objects without error
                fig = plot(raw_path, config_path, show=False)
                assert hasattr(fig, 'data')
                
                data = load_spice(raw_path)
                assert data == mock_data
                
                output_path = Path("test_output.yaml")
                create_config_template(output_path, raw_path)
                assert output_path.exists()
                cleanup_temp_file(str(output_path))
                
                warnings = validate_config(config_path, raw_path)
                assert warnings == []
                
        finally:
            cleanup_temp_file(raw_file_str)
            cleanup_temp_file(config_file_str) 