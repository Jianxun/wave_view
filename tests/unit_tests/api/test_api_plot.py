"""
Unit tests for wave_view API plot function.

Starting with basic functionality and building incrementally.
"""

import unittest
from unittest.mock import Mock, patch
import plotly.graph_objects as go
import numpy as np

from wave_view.api import plot
from wave_view.core.config import PlotConfig
from . import (
    create_temp_raw_file, cleanup_temp_file, create_mock_spice_plotter,
    get_basic_test_config, get_processed_data_config, get_test_processed_data
)


class TestPlotBasic(unittest.TestCase):
    """Test basic plot() function functionality."""
    
    @patch('wave_view.api.SpicePlotter')
    @patch('wave_view.api._configure_plotly_renderer')
    def test_plot_basic_functionality(self, mock_configure_renderer, mock_spice_plotter_class):
        """Test basic plot() function call with dictionary config."""
        # Set up mocks
        mock_figure = go.Figure()
        mock_figure.add_trace(go.Scatter(x=[1, 2, 3], y=[1, 2, 3], name="Test"))
        
        mock_plotter = create_mock_spice_plotter(return_figure=mock_figure)
        mock_spice_plotter_class.return_value = mock_plotter
        
        # Create temporary raw file for testing 
        temp_raw_file = create_temp_raw_file()
        
        try:
            # Test basic plot call
            config = get_basic_test_config()
            result = plot(temp_raw_file, config, show=False)
            
            # Verify results
            self.assertIsInstance(result, go.Figure)
            self.assertEqual(len(result.data), 1)  # Should have the test trace
            
            # Verify that the renderer was configured
            mock_configure_renderer.assert_called_once()
            
            # Verify SpicePlotter was created with the raw file
            mock_spice_plotter_class.assert_called_once_with(temp_raw_file)
            
            # Verify plotter methods were called
            # The API now converts dict configs to PlotConfig objects
            call_args = mock_plotter.load_config.call_args[0][0]
            self.assertIsInstance(call_args, PlotConfig)
            self.assertEqual(call_args.config["title"], config["title"])
            mock_plotter.create_figure.assert_called_once()
            
        finally:
            cleanup_temp_file(temp_raw_file)

    @patch('wave_view.api.SpicePlotter')
    @patch('wave_view.api._configure_plotly_renderer')
    def test_plot_with_show_true(self, mock_configure_renderer, mock_spice_plotter_class):
        """Test plot() function with show=True calls figure.show()."""
        # Set up mocks
        mock_figure = Mock(spec=go.Figure)
        mock_figure.data = [go.Scatter(x=[1, 2, 3], y=[1, 2, 3], name="Test")]
        
        mock_plotter = create_mock_spice_plotter(return_figure=mock_figure)
        mock_spice_plotter_class.return_value = mock_plotter
        
        # Create temporary raw file for testing 
        temp_raw_file = create_temp_raw_file()
        
        try:
            # Test plot call with show=True (default)
            config = get_basic_test_config()
            result = plot(temp_raw_file, config)  # show=True by default
            
            # Verify that figure.show() was called
            mock_figure.show.assert_called_once()
            
            # Verify the same figure was returned
            self.assertEqual(result, mock_figure)
            
        finally:
            cleanup_temp_file(temp_raw_file)

    @patch('wave_view.api.SpicePlotter')
    @patch('wave_view.api._configure_plotly_renderer')
    def test_plot_with_processed_data(self, mock_configure_renderer, mock_spice_plotter_class):
        """Test plot() function with processed_data parameter."""
        # Set up mocks
        mock_figure = go.Figure()
        mock_figure.add_trace(go.Scatter(x=[1, 2, 3], y=[1, 2, 3], name="Test"))
        
        mock_plotter = create_mock_spice_plotter(return_figure=mock_figure)
        mock_spice_plotter_class.return_value = mock_plotter
        
        # Create temporary raw file for testing 
        temp_raw_file = create_temp_raw_file()
        
        try:
            # Test plot call with processed data
            config = get_processed_data_config()
            processed_data = get_test_processed_data()
            
            result = plot(temp_raw_file, config, show=False, processed_data=processed_data)
            
            # Verify results
            self.assertIsInstance(result, go.Figure)
            
            # Verify processed signals were added to plotter
            # Check that processed data was added to the _processed_signals dict
            for signal_name, signal_array in processed_data.items():
                # The processed data should be converted to numpy arrays and stored
                stored_signal = mock_plotter._processed_signals[signal_name]
                self.assertIsInstance(stored_signal, np.ndarray)
                np.testing.assert_array_equal(stored_signal, signal_array)
            
            # Verify plotter methods were called
            # The API now converts dict configs to PlotConfig objects
            call_args = mock_plotter.load_config.call_args[0][0]
            self.assertIsInstance(call_args, PlotConfig)
            self.assertEqual(call_args.config["title"], config["title"])
            mock_plotter.create_figure.assert_called_once()
            
        finally:
            cleanup_temp_file(temp_raw_file)

    def test_plot_with_required_config(self):
        """Test plot() function requires config parameter."""
        # Create temporary raw file for testing 
        temp_raw_file = create_temp_raw_file()
        
        try:
            # Test that config=None raises TypeError
            with self.assertRaises(TypeError) as context:
                plot(temp_raw_file, config=None, show=False)
            
            error_message = str(context.exception)
            self.assertIn("config must be provided", error_message)
            
        finally:
            cleanup_temp_file(temp_raw_file)

if __name__ == '__main__':
    unittest.main()


class TestPlotErrorHandling(unittest.TestCase):
    """Test error handling in plot() function."""
    
    def test_plot_with_invalid_file_path(self):
        """Test plot() function with non-existent file path raises appropriate error."""
        # Test with non-existent file
        non_existent_file = "/path/that/does/not/exist.raw"
        config = get_basic_test_config()
        
        with self.assertRaises(FileNotFoundError) as context:
            plot(non_existent_file, config, show=False)
        
        # Verify the error message is user-friendly
        error_message = str(context.exception)
        self.assertIn("SPICE raw file not found", error_message)
        self.assertIn(non_existent_file, error_message)
    
    def test_plot_with_empty_file_path(self):
        """Test plot() function with empty file path raises appropriate error."""
        config = get_basic_test_config()
        
        with self.assertRaises(ValueError) as context:
            plot("", config, show=False)
        
        # Verify the error message is user-friendly
        error_message = str(context.exception)
        self.assertIn("file path cannot be empty", error_message)
    
    def test_plot_with_none_file_path(self):
        """Test plot() function with None file path raises appropriate error."""
        config = get_basic_test_config()
        
        with self.assertRaises(TypeError) as context:
            plot(None, config, show=False)
        
        # Verify the error message is user-friendly
        error_message = str(context.exception)
        self.assertIn("file path must be a string or Path object", error_message)
    
    @patch('wave_view.api.SpicePlotter')
    @patch('wave_view.api._configure_plotly_renderer')
    def test_plot_with_unused_kwargs(self, mock_configure_renderer, mock_spice_plotter_class):
        """Test plot() function with **kwargs to verify unused parameters raise TypeError."""
        # Set up mocks
        mock_figure = go.Figure()
        mock_figure.add_trace(go.Scatter(x=[1, 2, 3], y=[1, 2, 3], name="Test"))
        
        mock_plotter = create_mock_spice_plotter(return_figure=mock_figure)
        mock_spice_plotter_class.return_value = mock_plotter
        
        # Create temporary raw file for testing 
        temp_raw_file = create_temp_raw_file()
        
        try:
            config = get_basic_test_config()
            
            # Test with unused kwargs - should raise TypeError about unexpected keyword arguments
            with self.assertRaises(TypeError) as context:
                plot(temp_raw_file, config, show=False, unused_param="test", another_param=123)
            
            # Verify the error message mentions unexpected keyword arguments
            error_message = str(context.exception)
            self.assertTrue(
                "unexpected keyword argument" in error_message.lower() or 
                "got an unexpected keyword argument" in error_message.lower(),
                f"Error message should indicate unexpected keyword arguments: {error_message}"
            )
            
        finally:
            cleanup_temp_file(temp_raw_file)

    @patch('wave_view.api.SpicePlotter')
    @patch('wave_view.api._configure_plotly_renderer')
    def test_plot_with_invalid_processed_data_types(self, mock_configure_renderer, mock_spice_plotter_class):
        """Test plot() function with invalid processed_data parameter types."""
        # Set up mocks
        mock_figure = go.Figure()
        mock_figure.add_trace(go.Scatter(x=[1, 2, 3], y=[1, 2, 3], name="Test"))
        
        mock_plotter = create_mock_spice_plotter(return_figure=mock_figure)
        mock_spice_plotter_class.return_value = mock_plotter
        
        # Create temporary raw file for testing 
        temp_raw_file = create_temp_raw_file()
        
        try:
            config = get_basic_test_config()
            
            # Test with non-dict processed_data
            with self.assertRaises(TypeError) as context:
                plot(temp_raw_file, config, show=False, processed_data="not a dict")
            
            error_message = str(context.exception)
            self.assertIn("processed_data must be a dictionary", error_message)
            
            # Test with dict containing non-array values
            with self.assertRaises(TypeError) as context:
                plot(temp_raw_file, config, show=False, processed_data={"signal": "not an array"})
            
            error_message = str(context.exception)
            self.assertIn("signal values must be array-like", error_message)
            
        finally:
            cleanup_temp_file(temp_raw_file) 