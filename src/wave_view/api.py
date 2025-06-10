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


def plot(raw_file: str, 
         config: Union[str, Dict, None] = None,
         show: bool = True,
         processed_data: Optional[Dict[str, np.ndarray]] = None) -> go.Figure:
    """
    Simple plotting function for SPICE waveforms.
    
    This is the main API function that 90% of users will interact with.
    It provides a simple interface for creating waveform plots.
    
    Args:
        raw_file: Path to SPICE .raw file
        config: Configuration file path, dictionary, or None for auto-config
        show: Whether to display the plot immediately (default: True)
        processed_data: Optional dictionary of processed signals 
                       {signal_name: numpy_array}. These can be referenced
                       in config with "data.signal_name"
        
    Returns:
        Plotly Figure object
        
    Example:
        >>> import wave_view as wv
        >>> fig = wv.plot("simulation.raw", "config.yaml")
        >>> fig = wv.plot("simulation.raw", show=False)  # Return without showing
        
        # With processed data
        >>> import numpy as np
        >>> data = wv.load_spice("simulation.raw")
        >>> processed = {
        ...     "vdb_out": 20 * np.log10(np.abs(data.get_signal("v(out)"))),
        ...     "power": data.get_signal("v(vdd)") * data.get_signal("i(vdd)")
        ... }
        >>> config = '''
        ... title: "Analysis with Processed Data"
        ... X: {signal_key: "raw.time", label: "Time (s)"}
        ... Y:
        ...   - label: "Magnitude (dB)"
        ...     signals: {Output: "data.vdb_out"}
        ...   - label: "Power (W)"  
        ...     signals: {Supply: "data.power"}
        ... '''
        >>> fig = wv.plot("simulation.raw", config, processed_data=processed)
    """
    # Input validation
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
    
    # Handle configuration
    if config is None:
        # TODO: Implement auto-configuration based on common patterns
        # For now, create a basic config
        spice_data = plotter.data
        config = _create_auto_config(spice_data)
    
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


def create_config_template(output_path: Union[str, Path], 
                          raw_file: Optional[Union[str, Path]] = None,
                          signals: Optional[List[str]] = None) -> None:
    """
    Create a YAML configuration template file.
    
    Args:
        output_path: Path where to save the template (string or Path object)
        raw_file: Optional SPICE file to analyze for signal names (string or Path object)
        signals: Optional list of specific signals to include
        
    Example:
        >>> wv.create_config_template("my_config.yaml", "sim.raw")
        >>> wv.create_config_template("template.yaml", signals=["v(vdd)", "v(out)"])
        
        >>> from pathlib import Path
        >>> wv.create_config_template(Path("config.yaml"), Path("sim.raw"))
    """
    # Input validation for output_path
    if output_path is None:
        raise TypeError("output path must be a string or Path object, not None")
    
    if not isinstance(output_path, (str, Path)):
        raise TypeError("output path must be a string or Path object")
    
    if isinstance(output_path, str) and output_path.strip() == "":
        raise ValueError("output path cannot be empty")
    
    # Convert to Path for consistent handling
    output_file_path = Path(output_path)
    
    # Validate raw_file if provided
    raw_file_path = None
    if raw_file is not None:
        if not isinstance(raw_file, (str, Path)):
            raise TypeError("raw file path must be a string or Path object")
        
        if isinstance(raw_file, str) and raw_file.strip() == "":
            raise ValueError("raw file path cannot be empty")
        
        raw_file_path = Path(raw_file)
        
        # Check if raw file exists when provided
        if not raw_file_path.exists():
            raise FileNotFoundError(f"SPICE raw file not found: {raw_file_path}")
    
    # Create basic template
    template = {
        "title": "SPICE Waveform Plot",
        "source": "./simulation.raw",  # Relative path placeholder
        "X": {
            "signal_key": "raw.time",
            "label": "Time (s)"
        },
        "Y": []
    }
    
    # Add signals if provided
    if signals:
        voltage_signals = [s for s in signals if s.startswith('v(')]
        current_signals = [s for s in signals if s.startswith('i(')]
        
        if voltage_signals:
            template["Y"].append({
                "label": "Voltage (V)",
                "signals": {s: s for s in voltage_signals}
            })
        
        if current_signals:
            template["Y"].append({
                "label": "Current (A)", 
                "signals": {s: s for s in current_signals}
            })
        
        # Add any other signals
        other_signals = [s for s in signals if not s.startswith(('v(', 'i('))]
        if other_signals:
            template["Y"].append({
                "label": "Other Signals",
                "signals": {s: s for s in other_signals}
            })
    
    # Analyze raw file if provided
    elif raw_file_path:
        try:
            data = SpiceData(str(raw_file_path))
            template["source"] = str(raw_file_path)
            
            # Categorize signals
            voltage_signals = [s for s in data.signals if s.startswith('v(')][:5]  # Limit to first 5
            current_signals = [s for s in data.signals if s.startswith('i(')][:5]
            
            if voltage_signals:
                template["Y"].append({
                    "label": "Voltage (V)",
                    "signals": {s: s for s in voltage_signals}
                })
            
            if current_signals:
                template["Y"].append({
                    "label": "Current (A)",
                    "signals": {s: s for s in current_signals}
                })
                
        except Exception as e:
            print(f"Warning: Could not analyze raw file '{raw_file_path}': {e}")
            # Fall back to basic template
            
    # Ensure at least one Y axis
    if not template["Y"]:
        template["Y"].append({
            "label": "Signal",
            "signals": {"signal_name": "v(out)"}  # Placeholder
        })
    
    # Add optional settings with comments
    template.update({
        "plot_height": 600,
        "show_rangeslider": True,
        "show_zoom_buttons": True,
        "default_dragmode": "zoom"
    })
    
    # Write template
    with open(output_file_path, 'w') as f:
        yaml.dump(template, f, default_flow_style=False, sort_keys=False, indent=2)
    
    print(f"Configuration template created: {output_file_path}")


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


def _create_auto_config(spice_data: SpiceData) -> Dict[str, Any]:
    """
    Create automatic configuration based on signal analysis.
    
    Args:
        spice_data: SpiceData object to analyze
        
    Returns:
        Auto-generated configuration dictionary
    """
    signals = spice_data.signals
    
    # Basic auto-config
    config = {
        "title": "Auto-generated SPICE Plot",
        "X": {
            "signal_key": "raw.time",
            "label": "Time (s)"
        },
        "Y": []
    }
    
    # Find voltage and current signals
    voltage_signals = [s for s in signals if s.startswith('v(')][:3]  # Limit to 3
    current_signals = [s for s in signals if s.startswith('i(')][:2]  # Limit to 2
    
    if voltage_signals:
        config["Y"].append({
            "label": "Voltage (V)",
            "signals": {s: s for s in voltage_signals}
        })
    
    if current_signals:
        config["Y"].append({
            "label": "Current (A)",
            "signals": {s: s for s in current_signals}
        })
    
    # If no voltage/current signals found, use first few signals
    if not config["Y"]:
        first_signals = signals[:3]
        config["Y"].append({
            "label": "Signals",
            "signals": {s: s for s in first_signals}
        })
    
    return config 