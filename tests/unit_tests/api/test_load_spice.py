"""
Tests for load_spice() function.

This module tests the load_spice API function with comprehensive coverage of
functionality, error handling, and edge cases.
"""

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from wave_view.api import load_spice
from wave_view.core.reader import SpiceData
from . import (
    create_temp_raw_file, 
    cleanup_temp_file,
    create_mock_spice_data
)


class TestLoadSpiceBasicFunctionality:
    """Test basic functionality of load_spice function."""
    
    def test_load_spice_with_string_path(self):
        """Test load_spice with string file path."""
        # Create temporary file
        raw_file = create_temp_raw_file("test.raw")
        
        try:
            with patch('wave_view.api.SpiceData') as mock_spice_data_class:
                # Setup mock
                mock_data = create_mock_spice_data()
                mock_spice_data_class.return_value = mock_data
                
                # Call load_spice
                result = load_spice(raw_file)
                
                # Verify results
                assert result == mock_data
                mock_spice_data_class.assert_called_once_with(raw_file)
                
        finally:
            cleanup_temp_file(raw_file)
    
    def test_load_spice_with_path_object(self):
        """Test load_spice with Path object."""
        # Create temporary file
        raw_file_str = create_temp_raw_file("test.raw")
        raw_file_path = Path(raw_file_str)
        
        try:
            with patch('wave_view.api.SpiceData') as mock_spice_data_class:
                # Setup mock
                mock_data = create_mock_spice_data()
                mock_spice_data_class.return_value = mock_data
                
                # Call load_spice with Path object
                result = load_spice(raw_file_path)
                
                # Verify results
                assert result == mock_data
                # Should be called with string (converted internally)
                mock_spice_data_class.assert_called_once_with(raw_file_str)
                
        finally:
            cleanup_temp_file(raw_file_str)
    
    def test_load_spice_returns_spice_data_object(self):
        """Test that load_spice returns a SpiceData object with expected attributes."""
        # Create temporary file
        raw_file = create_temp_raw_file("test.raw")
        
        try:
            with patch('wave_view.api.SpiceData') as mock_spice_data_class:
                # Setup mock with realistic attributes
                mock_data = create_mock_spice_data(
                    signals=["time", "v(vdd)", "v(out)", "i(load)"],
                )
                mock_spice_data_class.return_value = mock_data
                
                # Call load_spice
                result = load_spice(raw_file)
                
                # Verify it's the expected SpiceData object
                assert result == mock_data
                assert hasattr(result, 'signals')
                assert hasattr(result, 'info')
                assert hasattr(result, 'get_signal')
                assert result.signals == ["time", "v(vdd)", "v(out)", "i(load)"]
                
        finally:
            cleanup_temp_file(raw_file)


class TestLoadSpiceInputValidation:
    """Test input validation and error handling."""
    
    def test_load_spice_none_input(self):
        """Test load_spice with None input."""
        with pytest.raises(TypeError, match="file path must be a string or Path object, not None"):
            load_spice(None)
    
    def test_load_spice_invalid_type_input(self):
        """Test load_spice with invalid type input."""
        with pytest.raises(TypeError, match="file path must be a string or Path object"):
            load_spice(123)
        
        with pytest.raises(TypeError, match="file path must be a string or Path object"):
            load_spice(['not', 'a', 'path'])
        
        with pytest.raises(TypeError, match="file path must be a string or Path object"):
            load_spice({'not': 'a path'})
    
    def test_load_spice_empty_string(self):
        """Test load_spice with empty string."""
        with pytest.raises(ValueError, match="file path cannot be empty"):
            load_spice("")
        
        with pytest.raises(ValueError, match="file path cannot be empty"):
            load_spice("   ")  # Whitespace only
    
    def test_load_spice_nonexistent_file_string(self):
        """Test load_spice with non-existent file (string path)."""
        with pytest.raises(FileNotFoundError, match="SPICE raw file not found"):
            load_spice("definitely_does_not_exist.raw")
    
    def test_load_spice_nonexistent_file_path_object(self):
        """Test load_spice with non-existent file (Path object)."""
        with pytest.raises(FileNotFoundError, match="SPICE raw file not found"):
            load_spice(Path("definitely_does_not_exist.raw"))


class TestLoadSpiceErrorHandling:
    """Test error handling when SpiceData raises exceptions."""
    
    def test_load_spice_spice_data_exception(self):
        """Test load_spice when SpiceData constructor raises exception."""
        # Create temporary file
        raw_file = create_temp_raw_file("test.raw")
        
        try:
            with patch('wave_view.api.SpiceData') as mock_spice_data_class:
                # Setup mock to raise exception
                mock_spice_data_class.side_effect = Exception("Corrupted SPICE file")
                
                # Call load_spice - should propagate the exception
                with pytest.raises(Exception, match="Corrupted SPICE file"):
                    load_spice(raw_file)
                
                # Verify SpiceData was called
                mock_spice_data_class.assert_called_once_with(raw_file)
                
        finally:
            cleanup_temp_file(raw_file)
    
    def test_load_spice_specific_spice_errors(self):
        """Test load_spice with specific SpiceData errors."""
        # Create temporary file
        raw_file = create_temp_raw_file("test.raw")
        
        try:
            # Test different types of exceptions that might come from SpiceData
            test_cases = [
                (ValueError("Invalid SPICE format"), "Invalid SPICE format"),
                (IOError("Cannot read file"), "Cannot read file"), 
                (RuntimeError("SPICE parsing error"), "SPICE parsing error"),
            ]
            
            for exception, expected_message in test_cases:
                with patch('wave_view.api.SpiceData') as mock_spice_data_class:
                    mock_spice_data_class.side_effect = exception
                    
                    with pytest.raises(type(exception), match=expected_message):
                        load_spice(raw_file)
                        
        finally:
            cleanup_temp_file(raw_file)


class TestLoadSpicePathHandling:
    """Test various path handling scenarios."""
    
    def test_load_spice_relative_path(self):
        """Test load_spice with relative path."""
        # Create a temporary file with a relative path structure
        import os
        import tempfile
        
        # Create a test file in the current directory to test relative paths
        test_filename = "test_relative.raw"
        
        # Make sure we clean up any existing test file
        if os.path.exists(test_filename):
            os.remove(test_filename)
        
        # Create the test file
        with open(test_filename, 'w') as f:
            f.write("test content")
        
        try:
            with patch('wave_view.api.SpiceData') as mock_spice_data_class:
                mock_data = create_mock_spice_data()
                mock_spice_data_class.return_value = mock_data
                
                result = load_spice(test_filename)
                
                assert result == mock_data
                # Should be called with the relative path (converted to string)
                mock_spice_data_class.assert_called_once_with(test_filename)
                
        finally:
            # Clean up the test file
            if os.path.exists(test_filename):
                os.remove(test_filename)
    
    def test_load_spice_absolute_path(self):
        """Test load_spice with absolute path."""
        # Create temporary file
        raw_file = create_temp_raw_file("test.raw")
        absolute_path = os.path.abspath(raw_file)
        
        try:
            with patch('wave_view.api.SpiceData') as mock_spice_data_class:
                mock_data = create_mock_spice_data()
                mock_spice_data_class.return_value = mock_data
                
                result = load_spice(absolute_path)
                
                assert result == mock_data
                mock_spice_data_class.assert_called_once_with(absolute_path)
                
        finally:
            cleanup_temp_file(raw_file)
    
    def test_load_spice_path_with_spaces(self):
        """Test load_spice with path containing spaces."""
        # Create temporary file with spaces in name
        with tempfile.NamedTemporaryFile(suffix='_test file.raw', delete=False) as temp_file:
            temp_path = temp_file.name
        
        try:
            with patch('wave_view.api.SpiceData') as mock_spice_data_class:
                mock_data = create_mock_spice_data()
                mock_spice_data_class.return_value = mock_data
                
                result = load_spice(temp_path)
                
                assert result == mock_data
                mock_spice_data_class.assert_called_once_with(temp_path)
                
        finally:
            cleanup_temp_file(temp_path)


class TestLoadSpiceIntegration:
    """Test integration scenarios and realistic usage patterns."""
    
    def test_load_spice_typical_workflow(self):
        """Test load_spice in a typical user workflow."""
        # Create temporary file
        raw_file = create_temp_raw_file("simulation.raw")
        
        try:
            with patch('wave_view.api.SpiceData') as mock_spice_data_class:
                # Setup realistic mock data
                mock_data = create_mock_spice_data(
                    signals=["time", "v(vdd)", "v(vss)", "v(out)", "v(in)", "i(vdd)", "i(load)"]
                )
                mock_spice_data_class.return_value = mock_data
                
                # Simulate typical user workflow
                data = load_spice(raw_file)
                
                # User would typically check signals
                assert "v(vdd)" in data.signals
                assert "i(vdd)" in data.signals
                assert len(data.signals) == 7
                
                # User would typically call get_signal
                mock_data.get_signal.assert_not_called()  # Not called yet
                
                # Simulate getting a signal
                time_data = data.get_signal("time")
                mock_data.get_signal.assert_called_with("time")
                
        finally:
            cleanup_temp_file(raw_file)
    
    def test_load_spice_multiple_files(self):
        """Test loading multiple SPICE files sequentially."""
        # Create multiple temporary files
        raw_files = [
            create_temp_raw_file("sim1.raw"),
            create_temp_raw_file("sim2.raw"),
            create_temp_raw_file("sim3.raw")
        ]
        
        try:
            with patch('wave_view.api.SpiceData') as mock_spice_data_class:
                # Setup different mock data for each file
                mock_data_objects = [
                    create_mock_spice_data(signals=["time", "v(out1)"]),
                    create_mock_spice_data(signals=["time", "v(out2)"]),
                    create_mock_spice_data(signals=["time", "v(out3)"])
                ]
                mock_spice_data_class.side_effect = mock_data_objects
                
                # Load each file
                data_objects = []
                for raw_file in raw_files:
                    data = load_spice(raw_file)
                    data_objects.append(data)
                
                # Verify all loaded correctly
                assert len(data_objects) == 3
                assert mock_spice_data_class.call_count == 3
                
                # Verify each call
                for i, raw_file in enumerate(raw_files):
                    mock_spice_data_class.assert_any_call(raw_file)
                    assert data_objects[i] == mock_data_objects[i]
                
        finally:
            for raw_file in raw_files:
                cleanup_temp_file(raw_file)


class TestLoadSpiceEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_load_spice_zero_byte_file(self):
        """Test load_spice with zero-byte file."""
        # Create empty file
        with tempfile.NamedTemporaryFile(suffix='.raw', delete=False) as temp_file:
            temp_path = temp_file.name
        
        try:
            with patch('wave_view.api.SpiceData') as mock_spice_data_class:
                # SpiceData might raise an exception for empty file
                mock_spice_data_class.side_effect = ValueError("Empty SPICE file")
                
                with pytest.raises(ValueError, match="Empty SPICE file"):
                    load_spice(temp_path)
                    
        finally:
            cleanup_temp_file(temp_path)
    
    def test_load_spice_very_long_path(self):
        """Test load_spice with very long file path."""
        # Create a file with a long name (but within OS limits)
        long_name = "a" * 100 + ".raw"
        raw_file = create_temp_raw_file(long_name)
        
        try:
            with patch('wave_view.api.SpiceData') as mock_spice_data_class:
                mock_data = create_mock_spice_data()
                mock_spice_data_class.return_value = mock_data
                
                result = load_spice(raw_file)
                
                assert result == mock_data
                mock_spice_data_class.assert_called_once_with(raw_file)
                
        finally:
            cleanup_temp_file(raw_file)
    
    def test_load_spice_special_characters_in_path(self):
        """Test load_spice with special characters in file path."""
        # Create file with special characters (that are valid in filenames)
        special_name = "test-file_123.raw"
        raw_file = create_temp_raw_file(special_name)
        
        try:
            with patch('wave_view.api.SpiceData') as mock_spice_data_class:
                mock_data = create_mock_spice_data()
                mock_spice_data_class.return_value = mock_data
                
                result = load_spice(raw_file)
                
                assert result == mock_data
                mock_spice_data_class.assert_called_once_with(raw_file)
                
        finally:
            cleanup_temp_file(raw_file) 