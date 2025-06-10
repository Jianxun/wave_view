"""
Main API functions for Wave View package.

This module provides the simple API functions that most users will interact with,
including the main plot() function and utility functions for configuration.
"""

from typing import Union, Dict, List, Optional, Any, Tuple
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
import yaml
from pathlib import Path

from .core.reader import SpiceData
from .core.config import PlotConfig
from .core.plotter import SpicePlotter


def config_from_file(file_path: Union[str, Path]) -> PlotConfig:
    """
    Create a plot configuration from a YAML file.
    
    Args:
        file_path: Path to YAML configuration file
        
    Returns:
        PlotConfig object
        
    Example:
        >>> import wave_view as wv
        >>> config = wv.config_from_file("analysis.yaml")
        >>> fig = wv.plot("simulation.raw", config)
    """
    if file_path is None:
        raise TypeError("file path must be a string or Path object, not None")
    
    if not isinstance(file_path, (str, Path)):
        raise TypeError("file path must be a string or Path object")
    
    if isinstance(file_path, str) and file_path.strip() == "":
        raise ValueError("file path cannot be empty")
    
    config_path = Path(file_path)
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    return PlotConfig(config_path)


def config_from_yaml(yaml_string: str) -> PlotConfig:
    """
    Create a plot configuration from a YAML string.
    
    Args:
        yaml_string: YAML configuration as a string
        
    Returns:
        PlotConfig object
        
    Example:
        >>> import wave_view as wv
        >>> config = wv.config_from_yaml('''
        ... title: "SPICE Analysis"
        ... X:
        ...   signal_key: "raw.time"
        ...   label: "Time (s)"
        ... Y:
        ...   - label: "Voltage (V)"
        ...     signals:
        ...       VDD: "v(vdd)"
        ... ''')
        >>> fig = wv.plot("simulation.raw", config)
    """
    if yaml_string is None:
        raise TypeError("YAML string cannot be None")
    
    if not isinstance(yaml_string, str):
        raise TypeError("YAML string must be a string")
    
    if yaml_string.strip() == "":
        raise ValueError("YAML string cannot be empty")
    
    try:
        config_dict = yaml.safe_load(yaml_string)
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Invalid YAML content: {e}")
    
    # Check for multi-figure configuration (YAML list) and reject it
    if isinstance(config_dict, list):
        raise ValueError(
            "Multi-figure configurations are no longer supported. "
            "The YAML string contains a list of figures. "
            "Please create separate YAML configurations for each figure and "
            "call plot() multiple times instead."
        )
    
    return PlotConfig(config_dict)


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
         config: Union[Dict, PlotConfig],
         show: bool = True,
         processed_data: Optional[Dict[str, np.ndarray]] = None) -> go.Figure:
    """
    Simple plotting function for SPICE waveforms.
    
    This is the main API function that provides a simple interface for creating 
    waveform plots with explicit configuration.
    
    Args:
        raw_file: Path to SPICE .raw file (string or Path object)
        config: PlotConfig object or configuration dictionary
        show: Whether to display the plot immediately (default: True)
        processed_data: Optional dictionary of processed signals 
                       {signal_name: numpy_array}. These can be referenced
                       in config with "data.signal_name"
        
    Returns:
        Plotly Figure object
        
    Example:
        >>> import wave_view as wv
        >>> 
        >>> # Using dictionary directly
        >>> config_dict = {
        ...     "title": "SPICE Analysis",
        ...     "X": {"signal_key": "raw.time", "label": "Time (s)"},
        ...     "Y": [{"label": "Voltage", "signals": {"VDD": "v(vdd)"}}]
        ... }
        >>> fig = wv.plot("simulation.raw", config_dict)
        >>> 
        >>> # Using factory functions (recommended)
        >>> config = wv.config_from_file("analysis.yaml")
        >>> fig = wv.plot("simulation.raw", config)
        >>> 
        >>> config = wv.config_from_yaml('''
        ... title: "My Analysis"
        ... X: {signal_key: "raw.time", label: "Time"}
        ... Y: [{label: "Voltage", signals: {VDD: "v(vdd)"}}]
        ... ''')
        >>> fig = wv.plot("simulation.raw", config)
        >>> 
        >>> # With processed data
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
        raise TypeError("config must be provided (PlotConfig object or dictionary)")
    
    if not isinstance(config, (dict, PlotConfig)):
        raise TypeError("config must be a PlotConfig object or dictionary. Use config_from_file(), config_from_yaml(), or config_from_dict() to create a PlotConfig.")
    
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
    
    # Load configuration
    if isinstance(config, dict):
        # Convert dict to PlotConfig
        plotter.load_config(PlotConfig(config))
    else:
        # Already a PlotConfig object
        plotter.load_config(config)
    
    # Create figure
    fig = plotter.create_figure()
    
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


def validate_config(config: Union[str, Path, Dict, PlotConfig], 
                   raw_file: Optional[Union[str, Path]] = None) -> List[str]:
    """
    Validate a configuration against optional SPICE data.
    
    Args:
        config: Configuration file path (string or Path object), dictionary, or PlotConfig object
        raw_file: Optional raw file to validate signals against (string or Path object)
        
    Returns:
        List of warning messages (empty if no warnings)
        
    Example:
        >>> # Using factory functions (recommended)
        >>> config = wv.config_from_file("config.yaml")
        >>> warnings = wv.validate_config(config, "simulation.raw")
        >>> if warnings:
        ...     for warning in warnings:
        ...         print(f"Warning: {warning}")
        
        >>> # Legacy support for file paths
        >>> warnings = wv.validate_config("config.yaml", "simulation.raw")
    """
    try:
        # Validate config parameter
        if config is None:
            raise TypeError("config must be a string, Path object, dictionary, or PlotConfig object, not None")
        
        # Handle different config types
        if isinstance(config, PlotConfig):
            plot_config = config
        elif isinstance(config, dict):
            plot_config = PlotConfig(config)
        elif isinstance(config, (str, Path)):
            # Legacy support - treat as file path
            if isinstance(config, str) and config.strip() == "":
                raise ValueError("config path cannot be empty")
            
            config_path = Path(config)
            if not config_path.exists():
                raise FileNotFoundError(f"Configuration file not found: {config_path}")
            
            plot_config = PlotConfig(config_path)
        else:
            raise TypeError("config must be a string, Path object, dictionary, or PlotConfig object")
        
        # Validate raw_file if provided
        spice_data = None
        if raw_file is not None:
            if not isinstance(raw_file, (str, Path)):
                raise TypeError("raw file path must be a string or Path object")
            
            if isinstance(raw_file, str) and raw_file.strip() == "":
                raise ValueError("raw file path cannot be empty")
            
            raw_file_path = Path(raw_file)
            if not raw_file_path.exists():
                raise FileNotFoundError(f"SPICE raw file not found: {raw_file_path}")
            
            spice_data = SpiceData(str(raw_file_path))
        
        return plot_config.validate(spice_data)
        
    except Exception as e:
        return [f"Configuration error: {e}"]




