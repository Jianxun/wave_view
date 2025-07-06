"""
API utility functions for Wave View package.

This module provides utility functions for data loading and environment configuration.
The main plot() function is directly exposed from core.plotting for maximum simplicity.
"""

from typing import Union, Dict, Optional, Any, Tuple
import numpy as np
import plotly.io as pio
from pathlib import Path

from .core.wavedataset import WaveDataset








def _configure_plotly_renderer() -> None:
    """
    Configure Plotly renderer based on environment.
    
    - Jupyter notebooks: Use default (inline) renderer
    - Standalone scripts: Use browser renderer
    """
    try:
        # Check if we're in a Jupyter environment
        if _is_jupyter_environment():
            # Let Plotly use its default renderer for notebooks (usually 'plotly_mimetype' or 'notebook')
            # Don't override the default
            pass
        else:
            # For standalone scripts, use browser
            pio.renderers.default = "browser"
    except Exception:
        # If we can't detect, default to browser (safer for standalone)
        pio.renderers.default = "browser"


def _is_jupyter_environment() -> bool:
    """
    Detect if we're running in a Jupyter environment.
    
    Returns:
        True if in Jupyter notebook/lab, False otherwise
    """
    try:
        # Check for IPython
        from IPython import get_ipython
        if get_ipython() is not None:
            # Check if it's a notebook environment
            ipython = get_ipython()
            if hasattr(ipython, 'kernel'):
                return True
    except ImportError:
        pass
    
    # Check for Google Colab
    try:
        import google.colab
        return True
    except ImportError:
        pass
    
    # Check for other notebook indicators
    try:
        import sys
        if 'ipykernel' in sys.modules:
            return True
    except:
        pass
    
    return False





def load_spice_raw(raw_file: Union[str, Path]) -> Tuple[Dict[str, np.ndarray], Dict[str, Any]]:
    """
    Load SPICE data from a raw file in v1.0.0 format.
    
    This function provides a convenient way to load SPICE data directly in the
    Dict[str, np.ndarray] format required by v1.0.0 plotting functions, along
    with any associated metadata.
    
    Args:
        raw_file: Path to SPICE .raw file (string or Path object)
        
    Returns:
        Tuple of (data, metadata) where:
        - data: Dict[str, np.ndarray] mapping signal names to numpy arrays
        - metadata: Dict[str, Any] with any associated metadata
        
    Example:
        >>> import wave_view as wv
        >>> data, metadata = wv.load_spice_raw("simulation.raw")
        >>> print(f"Loaded {len(data)} signals")
        >>> print(f"Available signals: {list(data.keys())}")
        >>> 
        >>> # Use directly with v1.0.0 plotting
        >>> spec = wv.PlotSpec.from_yaml("config.yaml")
        >>> fig = wv.plot_v1(data, spec)
        >>> fig.show()
    """
    # Input validation (same pattern as other functions)
    if raw_file is None:
        raise TypeError("file path must be a string or Path object, not None")
    
    if not isinstance(raw_file, (str, Path)):
        raise TypeError("file path must be a string or Path object")
    
    if isinstance(raw_file, str) and raw_file.strip() == "":
        raise ValueError("file path cannot be empty")
    
    # Convert to Path for consistent handling
    file_path = Path(raw_file)
    
    # Check if file exists
    if not file_path.exists():
        raise FileNotFoundError(f"SPICE raw file not found: {file_path}")
    
    # Load data using WaveDataset
    wave_data = WaveDataset.from_raw(str(file_path))
    
    # Convert all signals to Dict[str, np.ndarray] format
    data = {signal: wave_data.get_signal(signal) for signal in wave_data.signals}
    
    # Get metadata
    metadata = wave_data.metadata
    
    return data, metadata







