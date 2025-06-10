"""
Tests for plot_batch() function error handling improvements.

This module tests the enhanced plot_batch function with proper error reporting
and different error handling modes.
"""

import pytest
import tempfile
import os
from unittest.mock import Mock, patch
from pathlib import Path

from wave_view.api import plot_batch
from . import (
    create_temp_raw_file, 
    create_temp_yaml_config, 
    cleanup_temp_file,
    get_basic_test_config,
    create_mock_spice_plotter
)


class TestPlotBatchErrorHandling:
    """Test the error handling capabilities of plot_batch function."""
    
    def test_plot_batch_collect_mode_success(self):
        """Test plot_batch with collect mode when all plots succeed."""
        # Create temporary files
        raw_file1 = create_temp_raw_file("test1.raw")
        raw_file2 = create_temp_raw_file("test2.raw")
        config_file1 = create_temp_yaml_config(get_basic_test_config())
        config_file2 = create_temp_yaml_config(get_basic_test_config())
        
        try:
            with patch('wave_view.api.SpicePlotter') as mock_plotter_class:
                # Setup successful mock
                mock_plotter = create_mock_spice_plotter()
                mock_plotter_class.return_value = mock_plotter
                
                # Call plot_batch
                files_and_configs = [
                    (raw_file1, config_file1),
                    (raw_file2, config_file2)
                ]
                
                figures, errors = plot_batch(files_and_configs, error_handling="collect")
                
                # Verify results
                assert len(figures) == 2
                assert len(errors) == 0
                assert all(hasattr(fig, 'data') for fig in figures)  # Check if they're valid figures
                
        finally:
            # Cleanup
            for file_path in [raw_file1, raw_file2, config_file1, config_file2]:
                cleanup_temp_file(file_path)
    
    def test_plot_batch_collect_mode_partial_failures(self):
        """Test plot_batch with collect mode when some plots fail."""
        # Create temporary files
        raw_file1 = create_temp_raw_file("test1.raw")
        raw_file2 = "nonexistent.raw"  # This will cause a failure
        config_file1 = create_temp_yaml_config(get_basic_test_config())
        config_file2 = create_temp_yaml_config(get_basic_test_config())
        
        try:
            with patch('wave_view.api.SpicePlotter') as mock_plotter_class:
                # Setup mock to succeed for first file only  
                mock_plotter = create_mock_spice_plotter()
                mock_plotter_class.return_value = mock_plotter
                
                # Call plot_batch
                files_and_configs = [
                    (raw_file1, config_file1),
                    (raw_file2, config_file2)  # This will fail
                ]
                
                figures, errors = plot_batch(files_and_configs, error_handling="collect")
                
                # Verify results
                assert len(figures) == 1  # One success
                assert len(errors) == 1   # One failure
                
                # Check error structure
                error = errors[0]
                assert error['file'] == raw_file2
                assert error['config'] == config_file2
                assert 'not found' in error['error'].lower()
                
        finally:
            # Cleanup
            for file_path in [raw_file1, config_file1, config_file2]:
                cleanup_temp_file(file_path)
    
    def test_plot_batch_raise_mode_success(self):
        """Test plot_batch with raise mode when all plots succeed."""
        # Create temporary files
        raw_file1 = create_temp_raw_file("test1.raw")
        config_file1 = create_temp_yaml_config(get_basic_test_config())
        
        try:
            with patch('wave_view.api.SpicePlotter') as mock_plotter_class:
                # Setup successful mock
                mock_plotter = create_mock_spice_plotter()
                mock_plotter_class.return_value = mock_plotter
                
                # Call plot_batch
                files_and_configs = [(raw_file1, config_file1)]
                
                figures = plot_batch(files_and_configs, error_handling="raise")
                
                # Verify results
                assert len(figures) == 1
                assert hasattr(figures[0], 'data')  # Check if it's a valid figure
                
        finally:
            # Cleanup
            cleanup_temp_file(raw_file1)
            cleanup_temp_file(config_file1)
    
    def test_plot_batch_raise_mode_failure(self):
        """Test plot_batch with raise mode when a plot fails."""
        # Create temporary files
        raw_file1 = create_temp_raw_file("test1.raw")
        raw_file2 = "nonexistent.raw"  # This will cause a failure
        config_file1 = create_temp_yaml_config(get_basic_test_config())
        config_file2 = create_temp_yaml_config(get_basic_test_config())
        
        try:
            with patch('wave_view.api.SpicePlotter') as mock_plotter_class:
                # Setup mock
                mock_plotter = create_mock_spice_plotter()
                mock_plotter_class.return_value = mock_plotter
                
                # Call plot_batch - should raise exception
                files_and_configs = [
                    (raw_file1, config_file1),
                    (raw_file2, config_file2)  # This will fail
                ]
                
                with pytest.raises(Exception) as exc_info:
                    plot_batch(files_and_configs, error_handling="raise")
                
                # Verify exception message contains details
                assert "Failed to plot" in str(exc_info.value)
                assert "nonexistent.raw" in str(exc_info.value)
                
        finally:
            # Cleanup
            for file_path in [raw_file1, config_file1, config_file2]:
                cleanup_temp_file(file_path)
    
    def test_plot_batch_skip_mode_legacy_behavior(self, capsys):
        """Test plot_batch with skip mode preserves legacy print behavior."""
        # Create temporary files
        raw_file1 = create_temp_raw_file("test1.raw")
        raw_file2 = "nonexistent.raw"  # This will cause a failure
        config_file1 = create_temp_yaml_config(get_basic_test_config())
        config_file2 = create_temp_yaml_config(get_basic_test_config())
        
        try:
            with patch('wave_view.api.SpicePlotter') as mock_plotter_class:
                # Setup mock
                mock_plotter = create_mock_spice_plotter()
                mock_plotter_class.return_value = mock_plotter
                
                # Call plot_batch
                files_and_configs = [
                    (raw_file1, config_file1),
                    (raw_file2, config_file2)  # This will fail
                ]
                
                figures = plot_batch(files_and_configs, error_handling="skip")
                
                # Verify results
                assert len(figures) == 1  # One success
                
                # Check that error was printed (legacy behavior)
                captured = capsys.readouterr()
                assert "Error plotting" in captured.out
                assert "nonexistent.raw" in captured.out
                
        finally:
            # Cleanup
            for file_path in [raw_file1, config_file1, config_file2]:
                cleanup_temp_file(file_path)
    
    def test_plot_batch_default_behavior_is_collect(self):
        """Test that the default error_handling mode is 'collect'."""
        # Create temporary file (success case)
        raw_file = create_temp_raw_file("test.raw")
        config_file = create_temp_yaml_config(get_basic_test_config())
        
        try:
            with patch('wave_view.api.SpicePlotter') as mock_plotter_class:
                # Setup successful mock
                mock_plotter = create_mock_spice_plotter()
                mock_plotter_class.return_value = mock_plotter
                
                # Call plot_batch without specifying error_handling
                files_and_configs = [(raw_file, config_file)]
                
                result = plot_batch(files_and_configs)
                
                # Should return tuple (figures, errors) - not just figures
                assert isinstance(result, tuple)
                assert len(result) == 2
                figures, errors = result
                assert len(figures) == 1
                assert len(errors) == 0
                
        finally:
            # Cleanup
            cleanup_temp_file(raw_file)
            cleanup_temp_file(config_file) 