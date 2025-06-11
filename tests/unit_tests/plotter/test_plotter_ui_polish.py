"""
Tests for UI polish improvements in SpicePlotter.

This module tests:
1. Fixed Zoom XY functionality 
2. Title alignment (center positioning)
3. Zoom button configuration options
"""

import pytest
import plotly.graph_objects as go
from unittest.mock import Mock
import numpy as np

from wave_view.core.plotter import SpicePlotter
from wave_view.core.config import PlotConfig


class TestZoomFunctionality:
    """Test zoom button functionality improvements."""
    
    def test_zoom_xy_button_resets_all_fixedrange_properties(self):
        """Test that Zoom XY button properly resets all fixedrange properties."""
        # Setup
        plotter = SpicePlotter()
        
        # Mock SPICE data
        mock_spice_data = Mock()
        mock_spice_data.get_signal.return_value = np.array([1, 2, 3, 4, 5])
        plotter._spice_data = mock_spice_data
        
        # Configuration with zoom buttons enabled
        config_dict = {
            "title": "Zoom XY Test",
            "X": {"signal_key": "time", "label": "Time (s)"},
            "Y": [
                {"label": "Voltage", "signals": {"V1": "v(out)"}},
                {"label": "Current", "signals": {"I1": "i(vdd)"}}
            ],
            "show_zoom_buttons": True
        }
        
        plotter._config = PlotConfig(config_dict)
        
        # Create figure
        fig = plotter.create_figure()
        
        # Verify zoom buttons exist
        assert hasattr(fig.layout, 'updatemenus')
        assert len(fig.layout.updatemenus) == 1
        
        # Get the zoom buttons
        zoom_menu = fig.layout.updatemenus[0]
        assert len(zoom_menu.buttons) == 3
        
        # Test Zoom XY button (first button)
        zoom_xy_button = zoom_menu.buttons[0]
        assert zoom_xy_button.label == "Zoom XY"
        
        # Check that Zoom XY button resets all fixedrange properties
        zoom_xy_args = zoom_xy_button.args[0]
        assert zoom_xy_args["dragmode"] == "zoom"
        assert zoom_xy_args["xaxis.fixedrange"] is False
        assert zoom_xy_args["yaxis.fixedrange"] is False
        assert zoom_xy_args["yaxis2.fixedrange"] is False  # Second Y-axis
    
    def test_zoom_y_button_fixes_x_axis(self):
        """Test that Zoom Y button fixes X-axis and frees Y-axes."""
        # Setup
        plotter = SpicePlotter()
        
        # Mock SPICE data
        mock_spice_data = Mock()
        mock_spice_data.get_signal.return_value = np.array([1, 2, 3, 4, 5])
        plotter._spice_data = mock_spice_data
        
        # Configuration
        config_dict = {
            "title": "Zoom Y Test",
            "X": {"signal_key": "time", "label": "Time (s)"},
            "Y": [{"label": "Voltage", "signals": {"V1": "v(out)"}}],
            "show_zoom_buttons": True
        }
        
        plotter._config = PlotConfig(config_dict)
        
        # Create figure
        fig = plotter.create_figure()
        
        # Get Zoom Y button (second button)
        zoom_y_button = fig.layout.updatemenus[0].buttons[1]
        assert zoom_y_button.label == "Zoom Y"
        
        # Check Zoom Y button args
        zoom_y_args = zoom_y_button.args[0]
        assert zoom_y_args["dragmode"] == "zoom"
        assert zoom_y_args["xaxis.fixedrange"] is True  # X-axis fixed
        assert zoom_y_args["yaxis.fixedrange"] is False  # Y-axis free
    
    def test_zoom_x_button_fixes_y_axes(self):
        """Test that Zoom X button fixes Y-axes and frees X-axis."""
        # Setup
        plotter = SpicePlotter()
        
        # Mock SPICE data
        mock_spice_data = Mock()
        mock_spice_data.get_signal.return_value = np.array([1, 2, 3, 4, 5])
        plotter._spice_data = mock_spice_data
        
        # Configuration
        config_dict = {
            "title": "Zoom X Test",
            "X": {"signal_key": "time", "label": "Time (s)"},
            "Y": [{"label": "Voltage", "signals": {"V1": "v(out)"}}],
            "show_zoom_buttons": True
        }
        
        plotter._config = PlotConfig(config_dict)
        
        # Create figure
        fig = plotter.create_figure()
        
        # Get Zoom X button (third button)
        zoom_x_button = fig.layout.updatemenus[0].buttons[2]
        assert zoom_x_button.label == "Zoom X"
        
        # Check Zoom X button args
        zoom_x_args = zoom_x_button.args[0]
        assert zoom_x_args["dragmode"] == "zoom"
        assert zoom_x_args["xaxis.fixedrange"] is False  # X-axis free
        assert zoom_x_args["yaxis.fixedrange"] is True   # Y-axis fixed
    
    def test_zoom_buttons_disabled(self):
        """Test that zoom buttons are properly disabled when configured."""
        # Setup
        plotter = SpicePlotter()
        
        # Mock SPICE data
        mock_spice_data = Mock()
        mock_spice_data.get_signal.return_value = np.array([1, 2, 3, 4, 5])
        plotter._spice_data = mock_spice_data
        
        # Configuration with zoom buttons disabled
        config_dict = {
            "title": "No Zoom Buttons",
            "X": {"signal_key": "time", "label": "Time (s)"},
            "Y": [{"label": "Voltage", "signals": {"V1": "v(out)"}}],
            "show_zoom_buttons": False
        }
        
        plotter._config = PlotConfig(config_dict)
        
        # Create figure
        fig = plotter.create_figure()
        
        # Verify no zoom buttons
        assert not hasattr(fig.layout, 'updatemenus') or not fig.layout.updatemenus


class TestTitleAlignment:
    """Test title alignment functionality."""
    
    def test_default_title_center_alignment(self):
        """Test that titles are centered by default."""
        # Setup
        plotter = SpicePlotter()
        
        # Mock SPICE data
        mock_spice_data = Mock()
        mock_spice_data.get_signal.return_value = np.array([1, 2, 3, 4, 5])
        plotter._spice_data = mock_spice_data
        
        # Configuration with default title settings
        config_dict = {
            "title": "Centered Title Test",
            "X": {"signal_key": "time", "label": "Time (s)"},
            "Y": [{"label": "Voltage", "signals": {"V1": "v(out)"}}]
        }
        
        plotter._config = PlotConfig(config_dict)
        
        # Create figure
        fig = plotter.create_figure()
        
        # Check title alignment
        assert fig.layout.title.text == "Centered Title Test"
        assert fig.layout.title.x == 0.5        # Centered position
        assert fig.layout.title.xanchor == "center"  # Center anchor
    
    def test_custom_title_alignment(self):
        """Test custom title alignment configuration."""
        # Setup
        plotter = SpicePlotter()
        
        # Mock SPICE data
        mock_spice_data = Mock()
        mock_spice_data.get_signal.return_value = np.array([1, 2, 3, 4, 5])
        plotter._spice_data = mock_spice_data
        
        # Configuration with custom title alignment
        config_dict = {
            "title": "Left Aligned Title",
            "title_x": 0.0,
            "title_xanchor": "left",
            "X": {"signal_key": "time", "label": "Time (s)"},
            "Y": [{"label": "Voltage", "signals": {"V1": "v(out)"}}]
        }
        
        plotter._config = PlotConfig(config_dict)
        
        # Create figure
        fig = plotter.create_figure()
        
        # Check custom title alignment
        assert fig.layout.title.text == "Left Aligned Title"
        assert fig.layout.title.x == 0.0          # Left position
        assert fig.layout.title.xanchor == "left"  # Left anchor
    
    def test_right_aligned_title(self):
        """Test right-aligned title configuration."""
        # Setup
        plotter = SpicePlotter()
        
        # Mock SPICE data
        mock_spice_data = Mock()
        mock_spice_data.get_signal.return_value = np.array([1, 2, 3, 4, 5])
        plotter._spice_data = mock_spice_data
        
        # Configuration with right title alignment
        config_dict = {
            "title": "Right Aligned Title",
            "title_x": 1.0,
            "title_xanchor": "right",
            "X": {"signal_key": "time", "label": "Time (s)"},
            "Y": [{"label": "Voltage", "signals": {"V1": "v(out)"}}]
        }
        
        plotter._config = PlotConfig(config_dict)
        
        # Create figure
        fig = plotter.create_figure()
        
        # Check right title alignment
        assert fig.layout.title.text == "Right Aligned Title"
        assert fig.layout.title.x == 1.0           # Right position
        assert fig.layout.title.xanchor == "right"  # Right anchor


class TestUIPolishIntegration:
    """Test integration of UI polish features."""
    
    def test_zoom_and_title_together(self):
        """Test that zoom buttons and title alignment work together."""
        # Setup
        plotter = SpicePlotter()
        
        # Mock SPICE data
        mock_spice_data = Mock()
        mock_spice_data.get_signal.return_value = np.array([1, 2, 3, 4, 5])
        plotter._spice_data = mock_spice_data
        
        # Configuration with both features
        config_dict = {
            "title": "Integration Test",
            "title_x": 0.5,
            "title_xanchor": "center",
            "X": {"signal_key": "time", "label": "Time (s)"},
            "Y": [{"label": "Voltage", "signals": {"V1": "v(out)"}}],
            "show_zoom_buttons": True
        }
        
        plotter._config = PlotConfig(config_dict)
        
        # Create figure
        fig = plotter.create_figure()
        
        # Verify both features work
        # Title alignment
        assert fig.layout.title.text == "Integration Test"
        assert fig.layout.title.x == 0.5
        assert fig.layout.title.xanchor == "center"
        
        # Zoom buttons
        assert hasattr(fig.layout, 'updatemenus')
        assert len(fig.layout.updatemenus) == 1
        assert len(fig.layout.updatemenus[0].buttons) == 3
        assert fig.layout.updatemenus[0].buttons[0].label == "Zoom XY"
        
        # Verify Zoom XY works correctly
        zoom_xy_args = fig.layout.updatemenus[0].buttons[0].args[0]
        assert zoom_xy_args["xaxis.fixedrange"] is False
        assert zoom_xy_args["yaxis.fixedrange"] is False 