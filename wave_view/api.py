"""
Main API functions for Wave View package.

This module provides the simple API functions that most users will interact with,
including the main plot() function and utility functions for configuration.
"""

from typing import Union, Dict, List, Tuple, Optional, Any
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
         **kwargs) -> go.Figure:
    """
    Simple plotting function for SPICE waveforms.
    
    This is the main API function that 90% of users will interact with.
    It provides a simple interface for creating waveform plots.
    
    Args:
        raw_file: Path to SPICE .raw file
        config: Configuration file path, dictionary, or None for auto-config
        show: Whether to display the plot immediately (default: True)
        **kwargs: Additional arguments passed to the plotter
        
    Returns:
        Plotly Figure object
        
    Example:
        >>> import wave_view as wv
        >>> fig = wv.plot("simulation.raw", "config.yaml")
        >>> fig = wv.plot("simulation.raw", show=False)  # Return without showing
    """
    # Configure Plotly to open in browser (like prototype)
    pio.renderers.default = "browser"
    
    # Create plotter and load data
    plotter = SpicePlotter(raw_file)
    
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


def load_spice(raw_file: str) -> SpiceData:
    """
    Load SPICE data from a raw file.
    
    Args:
        raw_file: Path to SPICE .raw file
        
    Returns:
        SpiceData object for exploring signals and data
        
    Example:
        >>> data = wv.load_spice("simulation.raw")
        >>> print(data.signals)
        >>> print(data.info)
    """
    return SpiceData(raw_file)


def create_config_template(output_path: str, 
                          raw_file: Optional[str] = None,
                          signals: Optional[List[str]] = None) -> None:
    """
    Create a YAML configuration template file.
    
    Args:
        output_path: Path where to save the template
        raw_file: Optional SPICE file to analyze for signal names
        signals: Optional list of specific signals to include
        
    Example:
        >>> wv.create_config_template("my_config.yaml", "sim.raw")
        >>> wv.create_config_template("template.yaml", signals=["v(vdd)", "v(out)"])
    """
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
    elif raw_file:
        try:
            data = SpiceData(raw_file)
            template["source"] = raw_file
            
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
            print(f"Warning: Could not analyze raw file '{raw_file}': {e}")
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
    with open(output_path, 'w') as f:
        yaml.dump(template, f, default_flow_style=False, sort_keys=False, indent=2)
    
    print(f"Configuration template created: {output_path}")


def validate_config(config: Union[str, Dict], 
                   raw_file: Optional[str] = None) -> List[str]:
    """
    Validate a configuration against optional SPICE data.
    
    Args:
        config: Configuration file path or dictionary
        raw_file: Optional raw file to validate signals against
        
    Returns:
        List of warning messages (empty if no warnings)
        
    Example:
        >>> warnings = wv.validate_config("config.yaml", "simulation.raw")
        >>> if warnings:
        ...     for warning in warnings:
        ...         print(f"Warning: {warning}")
    """
    try:
        plot_config = PlotConfig(config)
        
        spice_data = None
        if raw_file:
            spice_data = SpiceData(raw_file)
        
        return plot_config.validate(spice_data)
        
    except Exception as e:
        return [f"Configuration error: {e}"]


def plot_batch(files_and_configs: List[Tuple[str, str]], 
               layout: str = "separate") -> List[go.Figure]:
    """
    Plot multiple SPICE files with their configurations.
    
    Args:
        files_and_configs: List of (raw_file, config_file) tuples
        layout: Layout style - "separate" or "grid" (future implementation)
        
    Returns:
        List of Plotly Figure objects
        
    Example:
        >>> figures = wv.plot_batch([
        ...     ("sim1.raw", "config1.yaml"),
        ...     ("sim2.raw", "config2.yaml")
        ... ])
    """
    figures = []
    
    for raw_file, config_file in files_and_configs:
        try:
            fig = plot(raw_file, config_file, show=False)
            figures.append(fig)
        except Exception as e:
            print(f"Error plotting {raw_file}: {e}")
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