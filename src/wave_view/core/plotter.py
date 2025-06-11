"""
Plotly-based plotting engine for SPICE waveforms.

This module provides the SpicePlotter class for creating interactive waveform
plots using Plotly, with support for multiple Y-axes, zoom controls, and 
custom signal processing.
"""

from typing import Dict, List, Optional, Callable, Union, Any
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio

from .reader import SpiceData
from .config import PlotConfig


class SpicePlotter:
    """
    Advanced Plotly-based plotter for SPICE waveforms.
    
    Provides a fluent API for loading data, configuring plots, adding processed
    signals, and creating interactive Plotly figures with multiple Y-axes and
    zoom controls.
    """
    
    def __init__(self, raw_file: Optional[str] = None):
        """
        Initialize SpicePlotter.
        
        Args:
            raw_file: Optional path to SPICE raw file to load immediately
        """
        self._spice_data: Optional[SpiceData] = None
        self._config: Optional[PlotConfig] = None
        self._processed_signals: Dict[str, np.ndarray] = {}
        
        if raw_file:
            self.load_data(raw_file)
    
    def load_data(self, raw_file: str) -> 'SpicePlotter':
        """
        Load SPICE data from raw file.
        
        Args:
            raw_file: Path to SPICE raw file
            
        Returns:
            Self for method chaining
        """
        self._spice_data = SpiceData(raw_file)
        return self
    
    def load_config(self, config: Union[str, Dict, PlotConfig]) -> 'SpicePlotter':
        """
        Load plot configuration.
        
        Args:
            config: Configuration file path, dictionary, or PlotConfig instance
            
        Returns:
            Self for method chaining
        """
        if isinstance(config, PlotConfig):
            self._config = config
        else:
            self._config = PlotConfig(config)
        return self
    
    def add_processed_signal(self, name: str, func: Callable[[Dict[str, np.ndarray]], np.ndarray]) -> 'SpicePlotter':
        """
        Add a processed signal computed from raw signals.
        
        Args:
            name: Name for the processed signal (used with "data.{name}" in config)
            func: Function that takes a dict of raw signals and returns processed data
            
        Returns:
            Self for method chaining
            
        Example:
            plotter.add_processed_signal("power", lambda d: d["v(vdd)"] * d["i(vdd)"])
        """
        if not self._spice_data:
            raise ValueError("Must load SPICE data before adding processed signals")
        
        # Get all available signals for the function
        signal_dict = {}
        for signal_name in self._spice_data.signals:
            signal_dict[signal_name] = self._spice_data.get_signal(signal_name)
        
        # Compute processed signal
        try:
            processed_data = func(signal_dict)
            self._processed_signals[name] = np.array(processed_data, dtype=float)
        except Exception as e:
            raise ValueError(f"Error computing processed signal '{name}': {e}")
        
        return self
    
    def create_figure(self, figure_index: int = 0) -> go.Figure:
        """
        Create a Plotly figure based on loaded data and configuration.
        
        Args:
            figure_index: Index of figure to create (deprecated, ignored)
            
        Returns:
            Plotly Figure object
            
        Raises:
            ValueError: If data or config not loaded
        """
        if not self._spice_data:
            raise ValueError("Must load SPICE data before creating figure")
        
        if not self._config:
            raise ValueError("Must load configuration before creating figure")
        
        # Get configuration (direct access for single-figure support)
        plot_config = self._config.config
        
        return self._create_plotly_figure(plot_config)
    
    def _create_plotly_figure(self, plot_config: Dict[str, Any]) -> go.Figure:
        """
        Create Plotly figure from configuration (adapted from prototype).
        
        Args:
            plot_config: Configuration dictionary for a single figure
            
        Returns:
            Plotly Figure object
        """
        def _get_signal_data(signal_key_str: str) -> np.ndarray:
            """Get signal data based on signal key string."""
            if not isinstance(signal_key_str, str):
                raise TypeError(f"Signal key must be a string, got {type(signal_key_str)}: {signal_key_str}")

            if signal_key_str.startswith("data."):
                data_dict_key = signal_key_str[5:]  # Remove "data."
                if data_dict_key not in self._processed_signals:
                    raise ValueError(
                        f"Processed signal '{data_dict_key}' not found. "
                        f"Available: {list(self._processed_signals.keys())}"
                    )
                return self._processed_signals[data_dict_key]
            else:
                # Handle raw signals (with or without "raw." prefix)
                trace_name = signal_key_str
                if signal_key_str.startswith("raw."):
                    trace_name = signal_key_str[4:]  # Remove "raw."
                
                signal_data = self._spice_data.get_signal(trace_name)
                
                # Convert complex signals to real for Plotly compatibility
                # For complex signals, take the real part (magnitude would be np.abs())
                if np.iscomplexobj(signal_data):
                    # For most cases like frequency, time, we want the real part
                    # For AC analysis voltages/currents, users should use processed_data for magnitude/phase
                    signal_data = np.real(signal_data)
                
                return signal_data

        fig = go.Figure()

        # Get X-axis data
        x_config = plot_config.get("X")
        if not x_config or not isinstance(x_config.get("signal_key"), str):
            raise ValueError("X-axis 'signal_key' must be specified in plot_config.")
        
        x_data = _get_signal_data(x_config["signal_key"])
        x_axis_title = x_config.get("label", x_config["signal_key"])

        # Prepare Y-axes (reverse order so first in config appears at top)
        y_axes_config = plot_config.get("Y", [])
        y_axes_config = list(reversed(y_axes_config))  # First in config → Top of plot
        num_y_axes = len(y_axes_config)
        if num_y_axes == 0:
            print("Warning: No Y axes defined in plot_config.")

        # Calculate Y-axis domains
        y_axis_domains = []
        if num_y_axes > 0:
            gap = 0.05  # Gap between y-axes (e.g., 5% of total height)
            total_gap_space = gap * (num_y_axes - 1) if num_y_axes > 1 else 0
            effective_plot_height = 1.0 - total_gap_space
            single_axis_height = effective_plot_height / num_y_axes

            current_bottom = 0
            for i in range(num_y_axes):
                domain_top = current_bottom + single_axis_height
                y_axis_domains.append([current_bottom, domain_top])
                current_bottom = domain_top + gap
        
        # Do NOT reverse - first Y-axis should be at bottom (domain starts at 0)
        # y_axis_domains.reverse()  # This was causing first Y-axis to appear at top

        layout_update_dict = {}
        plotly_y_axis_ids = []  # To keep track of yaxis, yaxis2, etc.

        # Configure Y-axes and add traces
        for i, y_axis_cfg in enumerate(y_axes_config):
            plotly_axis_id_num = i + 1
            plotly_axis_id_str = f"yaxis{plotly_axis_id_num if plotly_axis_id_num > 1 else ''}"
            plotly_y_axis_ids.append(plotly_axis_id_str)

            axis_layout_key = f"yaxis{plotly_axis_id_num}"

            y_axis_layout = {
                "title": y_axis_cfg.get("label", f"Y-Axis {plotly_axis_id_num}"),
                "domain": y_axis_domains[i],
                "anchor": "x"  # All y-axes anchor to x-axis for proper positioning
            }
            
            # Add log scale support for Y-axis
            if y_axis_cfg.get("scale") == "log":
                y_axis_layout["type"] = "log"
            
            layout_update_dict[axis_layout_key] = y_axis_layout

            # Add traces for this Y-axis
            for legend_name, signal_key_val in y_axis_cfg.get("signals", {}).items():
                y_data_for_trace = _get_signal_data(signal_key_val)
                fig.add_trace(go.Scatter(
                    x=x_data,
                    y=y_data_for_trace,
                    name=legend_name,
                    yaxis=f"y{plotly_axis_id_num}"
                ))

        # Global layout settings
        layout_update_dict["height"] = plot_config.get("plot_height", 600 if num_y_axes <= 1 else 300 * num_y_axes)
        layout_update_dict["dragmode"] = plot_config.get("default_dragmode", "zoom")

        x_axis_layout = {
            "title": x_axis_title,
            "rangeslider": {"visible": plot_config.get("show_rangeslider", True)},
            "domain": [0, 1]  # X-axis spans the full width
        }
        
        # Add log scale support for X-axis
        if x_config.get("scale") == "log":
            x_axis_layout["type"] = "log"
        
        layout_update_dict["xaxis"] = x_axis_layout

        # Configure zoom buttons
        if plot_config.get("show_zoom_buttons", True) and num_y_axes > 0:
            # Zoom XY (both X and Y axes free) - Fixed to reset fixedrange properties
            xy_zoom_args = {"dragmode": "zoom", "xaxis.fixedrange": False}
            for axis_id_str in plotly_y_axis_ids:
                xy_zoom_args[f"{axis_id_str}.fixedrange"] = False
            
            zoom_buttons = [
                dict(label="Zoom XY", method="relayout", args=[xy_zoom_args])
            ]

            # Zoom Y (all Y axes, X fixed)
            y_zoom_args = {"dragmode": "zoom", "xaxis.fixedrange": True}
            for axis_id_str in plotly_y_axis_ids:
                y_zoom_args[f"{axis_id_str}.fixedrange"] = False
            zoom_buttons.append(dict(label="Zoom Y", method="relayout", args=[y_zoom_args]))

            # Zoom X (X axis, Ys fixed)
            x_zoom_args = {"dragmode": "zoom", "xaxis.fixedrange": False}
            for axis_id_str in plotly_y_axis_ids:
                x_zoom_args[f"{axis_id_str}.fixedrange"] = True
            zoom_buttons.append(dict(label="Zoom X", method="relayout", args=[x_zoom_args]))

            layout_update_dict["updatemenus"] = [
                dict(
                    type="buttons",
                    direction="right",
                    x=0.5, xanchor="center",
                    y=1.15, yanchor="top",
                    showactive=True,
                    buttons=zoom_buttons
                )
            ]

        # Configure title alignment (center by default, configurable)
        title_text = plot_config.get("title", "SPICE Waveform Plot")
        title_x = plot_config.get("title_x", 0.5)  # Center by default
        title_xanchor = plot_config.get("title_xanchor", "center")  # Center anchor by default
        
        layout_update_dict["title"] = {
            "text": title_text,
            "x": title_x,
            "xanchor": title_xanchor
        }

        fig.update_layout(**layout_update_dict)
        return fig
    
    def show(self, figure_index: int = 0) -> None:
        """
        Create and display figure in browser or inline (environment-aware).
        
        Args:
            figure_index: Index of figure to show (deprecated, ignored)
        """
        # Import here to avoid circular import
        from ..api import _configure_plotly_renderer
        
        # Configure renderer based on environment
        _configure_plotly_renderer()
        
        fig = self.create_figure(figure_index)
        fig.show()
    
    @property
    def data(self) -> Optional[SpiceData]:
        """Get the loaded SPICE data."""
        return self._spice_data
    
    @property
    def config(self) -> Optional[PlotConfig]:
        """Get the loaded plot configuration."""
        return self._config
    
    @property
    def processed_signals(self) -> Dict[str, np.ndarray]:
        """Get dictionary of processed signals."""
        return self._processed_signals.copy()
    
    def __repr__(self) -> str:
        """String representation of SpicePlotter."""
        data_info = f"data loaded" if self._spice_data else "no data"
        config_info = f"config loaded" if self._config else "no config"
        processed_info = f"{len(self._processed_signals)} processed signals" if self._processed_signals else "no processed signals"
        return f"SpicePlotter({data_info}, {config_info}, {processed_info})" 