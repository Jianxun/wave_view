"""
Pydantic-based plot specification models.

This module provides PlotSpec and YAxisSpec classes that replace PlotConfig
with structured validation and type safety.
"""

from typing import List, Optional, Dict, Any, Union
from pathlib import Path
import yaml
import numpy as np
from pydantic import BaseModel, Field
import plotly.graph_objects as go


class YAxisSpec(BaseModel):
    """Y-axis configuration specification."""
    label: str = Field(..., description="Y-axis label")
    signals: Dict[str, str] = Field(..., description="Legend name -> signal key mapping")
    log_scale: bool = Field(False, description="Use logarithmic scale")
    unit: Optional[str] = Field(None, description="Unit for display")
    range: Optional[List[float]] = Field(None, description="[min, max] range")
    color: Optional[str] = Field(None, description="Axis color")


class PlotSpec(BaseModel):
    """
    Pydantic-based plot specification with fluent API.
    
    Replaces PlotConfig with structured validation and composable workflow.
    """
    # Core configuration
    x: str = Field(..., description="X-axis signal key (e.g., 'time', 'raw.frequency')")
    y: List[YAxisSpec] = Field(..., description="Y-axis specifications")
    title: Optional[str] = Field(None, description="Plot title")
    
    # Styling options
    width: Optional[int] = Field(None, description="Plot width in pixels")
    height: Optional[int] = Field(None, description="Plot height in pixels")
    theme: Optional[str] = Field("plotly", description="Plot theme")
    
    # Title positioning
    title_x: float = Field(0.5, description="Title x position (0=left, 0.5=center, 1=right)")
    title_xanchor: str = Field("center", description="Title anchor: left, center, right")
    
    # Advanced options
    show_legend: bool = Field(True, description="Show legend")
    grid: bool = Field(True, description="Show grid")
    zoom_buttons: bool = Field(True, description="Show zoom control buttons")
    
    # Factory methods
    @classmethod
    def from_yaml(cls, yaml_str: str) -> 'PlotSpec':
        """Create PlotSpec from YAML string."""
        try:
            config_dict = yaml.safe_load(yaml_str)
            if isinstance(config_dict, list):
                raise ValueError("Multi-figure configurations not supported")
            return cls.model_validate(config_dict)
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML: {e}")
    
    # Fluent API methods
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
        from .plotter import SpicePlotter
        
        # Create plotter with data
        plotter = SpicePlotter()
        plotter._spice_data = data
        plotter._processed_signals = processed_data or {}
        
        # Convert PlotSpec to legacy config format for SpicePlotter
        legacy_config = self._to_legacy_config()
        return plotter._create_plotly_figure(legacy_config)
    
    # Utility methods
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
            "height": self.height,
            "theme": self.theme,
            "title_x": self.title_x,
            "title_xanchor": self.title_xanchor,
            "show_legend": self.show_legend,
            "grid": self.grid,
            "zoom_buttons": self.zoom_buttons
        } 