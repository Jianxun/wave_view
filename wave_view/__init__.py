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
    create_config_template,
    validate_config,
    plot_batch
)

# Convenience imports for power users
from .core.plotter import SpicePlotter

__all__ = [
    # Main API
    'plot',
    'load_spice',
    'create_config_template', 
    'validate_config',
    'plot_batch',
    
    # Core classes
    'SpiceData',
    'SpicePlotter', 
    'PlotConfig',
] 