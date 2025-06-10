"""
Main API functions for Wave View package.

This module provides the simple API functions that most users will interact with,
including the main plot() function and utility functions for configuration.
"""

from typing import Union, Dict, List, Tuple, Optional, Any
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
import yaml
from pathlib import Path

from .core.reader import SpiceData
from .core.config import PlotConfig
from .core.plotter import SpicePlotter


def plot(raw_file: Union[str, Path], 
         config: Union[str, Path, Dict],
         show: bool = True,
         processed_data: Optional[Dict[str, np.ndarray]] = None) -> go.Figure:
    """
    Simple plotting function for SPICE waveforms.
    
    This is the main API function that provides a simple interface for creating 
    waveform plots with explicit configuration.
    
    Args:
        raw_file: Path to SPICE .raw file (string or Path object)
        config: Configuration file path (string or Path), or dictionary
        show: Whether to display the plot immediately (default: True)
        processed_data: Optional dictionary of processed signals 
                       {signal_name: numpy_array}. These can be referenced
                       in config with "data.signal_name"
        
    Returns:
        Plotly Figure object
        
    Example:
        >>> import wave_view as wv
        >>> config = {
        ...     "title": "SPICE Analysis",
        ...     "X": {"signal_key": "raw.time", "label": "Time (s)"},
        ...     "Y": [{"label": "Voltage", "signals": {"VDD": "v(vdd)"}}]
        ... }
        >>> fig = wv.plot("simulation.raw", config)
        
        # With YAML configuration file
        >>> fig = wv.plot("simulation.raw", "config.yaml")
        
        # With processed data
        >>> import numpy as np
        >>> data = wv.load_spice("simulation.raw")
        >>> processed = {
        ...     "vdb_out": 20 * np.log10(np.abs(data.get_signal("v(out)"))),
        ...     "power": data.get_signal("v(vdd)") * data.get_signal("i(vdd)")
        ... }
        >>> config = {
        ...     "title": "Analysis with Processed Data",
        ...     "X": {"signal_key": "raw.time", "label": "Time (s)"},
        ...     "Y": [
        ...         {"label": "Magnitude (dB)", "signals": {"Output": "data.vdb_out"}},
        ...         {"label": "Power (W)", "signals": {"Supply": "data.power"}}
        ...     ]
        ... }
        >>> fig = wv.plot("simulation.raw", config, processed_data=processed)
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
        raise TypeError("config must be provided (string, Path, or dictionary)")
    
    if not isinstance(config, (str, Path, dict)):
        raise TypeError("config must be a string, Path object, or dictionary")
    
    # Additional validation for string/Path config
    if isinstance(config, (str, Path)):
        if isinstance(config, str) and config.strip() == "":
            raise ValueError("config path cannot be empty")
        
        config_path = Path(config)
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    # Validate processed_data parameter
    if processed_data is not None:
        if not isinstance(processed_data, dict):
            raise TypeError("processed_data must be a dictionary of signal names to arrays")
        
        for signal_name, signal_array in processed_data.items():
            if not isinstance(signal_name, str):
                raise TypeError("processed_data keys (signal names) must be strings")
            
            # Check if the value is array-like but not a string
            if isinstance(signal_array, str):
                raise TypeError(f"signal values must be array-like (lists, numpy arrays, etc.), got string for signal '{signal_name}'")
            
            # Check if the value is array-like (has __len__ and __getitem__)
            if not hasattr(signal_array, '__len__') or not hasattr(signal_array, '__getitem__'):
                raise TypeError(f"signal values must be array-like (lists, numpy arrays, etc.), got {type(signal_array).__name__} for signal '{signal_name}'")
    
    # Auto-detect environment and set appropriate renderer
    _configure_plotly_renderer()
    
    # Create plotter and load data
    plotter = SpicePlotter(str(file_path))
    
    # Add processed signals if provided
    if processed_data:
        for signal_name, signal_array in processed_data.items():
            if not isinstance(signal_array, np.ndarray):
                signal_array = np.array(signal_array, dtype=float)
            plotter._processed_signals[signal_name] = signal_array
    
    # Load configuration (no auto-config)
    plotter.load_config(config)
    
    # Create figure
    fig = plotter.create_figure()
    
    if show:
        fig.show()
    
    return fig


def _configure_plotly_renderer():
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
    voltage_signals = [s for s in signals if s.startswith('v(')]
    current_signals = [s for s in signals if s.startswith('i(')]
    other_signals = [s for s in signals if not s.startswith(('v(', 'i('))]
    
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


def validate_config(config: Union[str, Path, Dict], 
                   raw_file: Optional[Union[str, Path]] = None) -> List[str]:
    """
    Validate a configuration against optional SPICE data.
    
    Args:
        config: Configuration file path (string or Path object) or dictionary
        raw_file: Optional raw file to validate signals against (string or Path object)
        
    Returns:
        List of warning messages (empty if no warnings)
        
    Example:
        >>> warnings = wv.validate_config("config.yaml", "simulation.raw")
        >>> if warnings:
        ...     for warning in warnings:
        ...         print(f"Warning: {warning}")
        
        >>> from pathlib import Path
        >>> warnings = wv.validate_config(Path("config.yaml"), Path("sim.raw"))
    """
    try:
        # Validate config parameter
        if config is None:
            raise TypeError("config must be a string, Path object, or dictionary, not None")
        
        if not isinstance(config, (str, Path, dict)):
            raise TypeError("config must be a string, Path object, or dictionary")
        
        # Additional validation for string/Path config
        if isinstance(config, (str, Path)):
            if isinstance(config, str) and config.strip() == "":
                raise ValueError("config path cannot be empty")
            
            config_path = Path(config)
            if not config_path.exists():
                raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        # Validate raw_file if provided
        validated_raw_file = None
        if raw_file is not None:
            if not isinstance(raw_file, (str, Path)):
                raise TypeError("raw file path must be a string or Path object")
            
            if isinstance(raw_file, str) and raw_file.strip() == "":
                raise ValueError("raw file path cannot be empty")
            
            raw_file_path = Path(raw_file)
            if not raw_file_path.exists():
                raise FileNotFoundError(f"SPICE raw file not found: {raw_file_path}")
            
            validated_raw_file = str(raw_file_path)
        
        plot_config = PlotConfig(config)
        
        spice_data = None
        if validated_raw_file:
            spice_data = SpiceData(validated_raw_file)
        
        return plot_config.validate(spice_data)
        
    except Exception as e:
        return [f"Configuration error: {e}"]


def plot_batch(files_and_configs: List[Tuple[str, str]], 
               layout: str = "separate",
               error_handling: str = "collect") -> Union[List[go.Figure], Tuple[List[go.Figure], List[Dict[str, str]]]]:
    """
    Plot multiple SPICE files with their configurations.
    
    Args:
        files_and_configs: List of (raw_file, config_file) tuples
        layout: Layout style - "separate" or "grid" (future implementation)
        error_handling: How to handle errors:
            - "collect": Collect errors and return them with figures (default)
            - "raise": Raise exception on first error
            - "skip": Skip errors silently and continue (legacy behavior)
        
    Returns:
        If error_handling is "collect": Tuple of (figures, errors)
            - figures: List of successful Plotly Figure objects
            - errors: List of error dictionaries with keys 'file', 'config', 'error'
        Otherwise: List of Plotly Figure objects
        
    Raises:
        Exception: If error_handling is "raise" and any plot fails
        
    Example:
        >>> # Collect errors (recommended)
        >>> figures, errors = wv.plot_batch([
        ...     ("sim1.raw", "config1.yaml"),
        ...     ("sim2.raw", "config2.yaml")
        ... ])
        >>> if errors:
        ...     print(f"Failed to plot {len(errors)} files:")
        ...     for error in errors:
        ...         print(f"  {error['file']}: {error['error']}")
        
        >>> # Raise on first error
        >>> figures = wv.plot_batch([
        ...     ("sim1.raw", "config1.yaml")
        ... ], error_handling="raise")
    """
    figures = []
    errors = []
    
    for raw_file, config_file in files_and_configs:
        try:
            fig = plot(raw_file, config_file, show=False)
            figures.append(fig)
        except Exception as e:
            error_info = {
                'file': raw_file,
                'config': config_file,
                'error': str(e)
            }
            
            if error_handling == "raise":
                raise Exception(f"Failed to plot {raw_file} with config {config_file}: {e}") from e
            elif error_handling == "skip":
                # Legacy behavior - just print and continue
                print(f"Error plotting {raw_file}: {e}")
                continue
            else:  # "collect" - default behavior
                errors.append(error_info)
                continue
    
    # Show all figures if layout is separate
    if layout == "separate":
        for fig in figures:
            fig.show()
    elif layout == "grid":
        # TODO: Implement subplot grid layout
        print("Grid layout not yet implemented, showing separate figures")
        for fig in figures:
            fig.show()
    
    # Return based on error handling mode
    if error_handling == "collect":
        return figures, errors
    else:
        return figures

