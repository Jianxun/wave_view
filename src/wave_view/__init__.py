"""
Wave View - SPICE Waveform Visualization Package

A Python package for visualizing SPICE simulation waveforms, designed primarily 
for Jupyter notebook integration with both simple plotting functions and advanced 
signal processing capabilities.
"""

__version__ = "0.1.0"
__author__ = "Wave View Development Team"

# Core classes
from .core.reader import SpiceData
from .core.plotter import SpicePlotter
from .core.config import PlotConfig

# Main API functions
from .api import (
    plot,
    load_spice,
    explore_signals,
    validate_config,
    config_from_file,
    config_from_yaml
)

# Convenience imports for power users
from .core.plotter import SpicePlotter

# Plotly imports for user access
import plotly.io as pio

def set_renderer(renderer: str = "auto"):
    """
    Set the Plotly renderer for Wave View plots.
    
    Args:
        renderer: Renderer type - "auto", "browser", "notebook", "plotly_mimetype", etc.
                 "auto" (default) detects environment automatically
    
    Example:
        >>> import wave_view as wv
        >>> wv.set_renderer("notebook")  # Force notebook inline display
        >>> wv.set_renderer("browser")   # Force browser display
        >>> wv.set_renderer("auto")      # Auto-detect (default)
    """
    if renderer == "auto":
        from .api import _configure_plotly_renderer
        _configure_plotly_renderer()
    else:
        pio.renderers.default = renderer
    
    print(f"📊 Plotly renderer set to: {pio.renderers.default}")

__all__ = [
    # Main API
    'plot',
    'load_spice',
    'explore_signals', 
    'validate_config',
    
    # Configuration factories
    'config_from_file',
    'config_from_yaml',
    
    # Core classes
    'SpiceData',
    'SpicePlotter', 
    'PlotConfig',
    
    # Utilities
    'set_renderer',
    'pio',  # Give users access to plotly.io
] 