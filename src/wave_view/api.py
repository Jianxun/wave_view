"""
Main API functions for Wave View package.

This module provides the simple API functions that most users will interact with,
including the main plot() function and utility functions for configuration.
"""

from typing import Union, Dict, List, Optional, Any, Tuple
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
from pathlib import Path

from .core.reader import SpiceData
from .core.plotspec import PlotSpec
from .core.plotting import plot as _plot_v1
from .core.wavedataset import WaveDataset


def _categorize_signals(signals: List[str]) -> Tuple[List[str], List[str], List[str]]:
    """
    Categorize SPICE signals into voltage, current, and other signals.
    
    This utility function separates signals based on their naming convention:
    - Voltage signals: start with 'v('
    - Current signals: start with 'i('  
    - Other signals: everything else
    
    Args:
        signals: List of signal names to categorize
        
    Returns:
        Tuple of (voltage_signals, current_signals, other_signals)
        
    Example:
        >>> signals = ['v(out)', 'i(r1)', 'freq', 'v(in)']
        >>> voltage, current, other = _categorize_signals(signals)
        >>> print(voltage)  # ['v(out)', 'v(in)']
        >>> print(current)  # ['i(r1)']
        >>> print(other)    # ['freq']
    """
    voltage_signals = [s for s in signals if s.startswith('v(')]
    current_signals = [s for s in signals if s.startswith('i(')]
    other_signals = [s for s in signals if not s.startswith(('v(', 'i('))]
    
    return voltage_signals, current_signals, other_signals


def plot(raw_file: Union[str, Path], 
         config: Union[Dict, PlotSpec],
         show: bool = True) -> go.Figure:
    """
    Simple plotting function for SPICE waveforms using v1.0.0 architecture.
    
    Args:
        raw_file: Path to SPICE .raw file (string or Path object)
        config: PlotSpec object or configuration dictionary
        show: Whether to display the plot immediately (default: True)
        
    Returns:
        Plotly Figure object
        
    Example:
        >>> import wave_view as wv
        >>> 
        >>> # Using PlotSpec (recommended)
        >>> spec = wv.PlotSpec.from_yaml('''
        ... title: "My Analysis"
        ... x: "time"
        ... y:
        ...   - label: "Voltage (V)"
        ...     signals:
        ...       Output: "v(out)"
        ... ''')
        >>> fig = wv.plot("simulation.raw", spec)
        >>> 
        >>> # Using dictionary directly
        >>> config_dict = {
        ...     "title": "SPICE Analysis",
        ...     "x": "time",
        ...     "y": [{
        ...         "label": "Voltage (V)",
        ...         "signals": {"VDD": "v(vdd)"}
        ...     }]
        ... }
        >>> fig = wv.plot("simulation.raw", config_dict)
    """
    # Input validation for raw_file
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
    
    # Input validation for config
    if config is None:
        raise TypeError("configuration cannot be None")
    
    if not isinstance(config, (dict, PlotSpec)):
        raise TypeError("configuration must be a dictionary or PlotSpec object")
    
    # Auto-detect environment and set appropriate renderer
    _configure_plotly_renderer()
    
    # Load SPICE data using v1.0.0 API
    data, metadata = load_spice_raw(raw_file)
    
    # Convert config to PlotSpec if needed
    if isinstance(config, dict):
        spec = PlotSpec.model_validate(config)
    else:
        spec = config
    
    # Create figure using v1.0.0 API
    fig = _plot_v1(data, spec)
    
    if show:
        fig.show()
    
    return fig


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


def load_spice(raw_file: Union[str, Path]) -> SpiceData:
    """
    Load SPICE data from a raw file.
    
    Args:
        raw_file: Path to SPICE .raw file (string or Path object)
        
    Returns:
        SpiceData object for exploring signals and data
        
    Example:
        >>> data = wv.load_spice("simulation.raw")
        >>> print(data.signals)
        >>> print(data.info)
        
        >>> from pathlib import Path
        >>> data = wv.load_spice(Path("simulation.raw"))
    """
    # Input validation (same pattern as plot function)
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
    
    return SpiceData(str(file_path))


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


def explore_signals(raw_file: Union[str, Path]) -> List[str]:
    """
    Explore and list all available signals in a SPICE raw file.
    
    This function provides signal discovery - showing what signals are available
    in the raw file so users can make informed decisions about configuration.
    
    Args:
        raw_file: Path to SPICE .raw file (string or Path object)
        
    Returns:
        List of available signal names
        
    Example:
        >>> import wave_view as wv
        >>> signals = wv.explore_signals("simulation.raw")
        >>> print("Available signals:")
        >>> for signal in signals:
        ...     print(f"  - {signal}")
        
        >>> from pathlib import Path
        >>> signals = wv.explore_signals(Path("sim.raw"))
    """
    # Input validation for raw_file
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
    
    # Load data and get signals
    spice_data = SpiceData(str(file_path))
    signals = spice_data.signals
    
    # Print signals for immediate visibility (placeholder behavior)
    print(f"\nAvailable signals in '{file_path}':")
    print("=" * 50)
    
    # Categorize signals for better readability
    voltage_signals, current_signals, other_signals = _categorize_signals(signals)
    
    if voltage_signals:
        print(f"Voltage signals ({len(voltage_signals)}):")
        for signal in voltage_signals:
            print(f"  - {signal}")
        print()
    
    if current_signals:
        print(f"Current signals ({len(current_signals)}):")
        for signal in current_signals:
            print(f"  - {signal}")
        print()
    
    if other_signals:
        print(f"Other signals ({len(other_signals)}):")
        for signal in other_signals:
            print(f"  - {signal}")
        print()
    
    print(f"Total: {len(signals)} signals")
    print("=" * 50)
    
    return signals




