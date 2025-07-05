"""
Archive of PlotSpec v0.2.0 implementation methods.

This file preserves the plotting methods that will be removed in v1.0.0
architecture. These methods can be referenced when implementing the new
standalone plotting functions.

Archived methods:
- plot()
- show()
- get_figure() 
- _to_legacy_config()
"""

from typing import List, Optional, Dict, Any, Union
from pathlib import Path
import yaml
import numpy as np
from pydantic import BaseModel, Field
import plotly.graph_objects as go


class ArchivedPlotSpecMethods:
    """Archived methods from PlotSpec v0.2.0 implementation."""
    
    def plot(self, data, processed_data: Optional[Dict[str, np.ndarray]] = None) -> go.Figure:
        """
        Create and return Plotly figure.
        
        Args:
            data: SpiceData object (pre-loaded)
            processed_data: Optional processed signals dictionary
            
        Returns:
            Plotly Figure object
        """
        # Import here to avoid circular imports
        from ..core.plotter import SpicePlotter
        
        # Create plotter with data
        plotter = SpicePlotter()
        plotter._spice_data = data
        plotter._processed_signals = processed_data or {}
        
        # Convert PlotSpec to legacy config format for SpicePlotter
        legacy_config = self._to_legacy_config()
        return plotter._create_plotly_figure(legacy_config)
    
    def get_figure(self, data, processed_data: Optional[Dict[str, np.ndarray]] = None) -> go.Figure:
        """
        Get the Plotly figure (alias for plot() method).
        
        Args:
            data: SpiceData object (pre-loaded)
            processed_data: Optional processed signals dictionary
            
        Returns:
            Plotly Figure object
        """
        return self.plot(data, processed_data)
    
    def show(self, data, processed_data: Optional[Dict[str, np.ndarray]] = None) -> None:
        """
        Create and display the plot directly.
        
        Args:
            data: SpiceData object (pre-loaded)
            processed_data: Optional processed signals dictionary
        """
        fig = self.plot(data, processed_data)
        fig.show()
    
    def _to_legacy_config(self) -> Dict[str, Any]:
        """Convert PlotSpec to legacy PlotConfig format for SpicePlotter."""
        return {
            "title": self.title,
            "X": {"signal_key": self.x, "label": self.x},
            "Y": [
                {
                    "label": y_spec.label,
                    "signals": y_spec.signals,
                    "log_scale": y_spec.log_scale,
                    "unit": y_spec.unit,
                    "range": y_spec.range,
                    "color": y_spec.color
                }
                for y_spec in self.y
            ],
            "width": self.width,
            "plot_height": self.height,  # Map to legacy field name
            "theme": self.theme,
            "title_x": self.title_x,
            "title_xanchor": self.title_xanchor,
            "show_legend": self.show_legend,
            "grid": self.grid,
            "show_zoom_buttons": self.zoom_buttons,  # Map to legacy field name
            "zoom_buttons_x": self.zoom_buttons_x,
            "zoom_buttons_y": self.zoom_buttons_y,
            "show_rangeslider": self.show_rangeslider
        }


# Example usage patterns for reference when implementing new plotting functions:
"""
# v0.2.0 usage pattern (archived)
spec = PlotSpec.from_yaml(config_yaml)
fig = spec.plot(data)
fig.show()

# v1.0.0 usage pattern (new)
spec = wv.PlotSpec.from_yaml(config_yaml)
fig = wv.plot(data, spec)
fig.show()
""" 