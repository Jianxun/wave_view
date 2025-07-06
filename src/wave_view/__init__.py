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
from .core.plotspec import PlotSpec
from .core.wavedataset import WaveDataset

# Main API functions
from .core.plotting import plot
from .api import load_spice_raw

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
    'load_spice_raw',
    
    # Core classes
    'SpiceData',
    'PlotSpec',
    'WaveDataset',
    
    # Utilities
    'set_renderer',
    'pio',  # Give users access to plotly.io
]

# Configure Plotly renderer automatically on import
# This eliminates the need for manual renderer configuration in user code
try:
    from .api import _configure_plotly_renderer
    _configure_plotly_renderer()
except Exception:
    # If auto-detection fails, default to browser (safe fallback)
    pio.renderers.default = "browser" 