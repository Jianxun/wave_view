"""
v1.0.0 Standalone plotting functions.

This module provides standalone plotting functions that work with
Dict[str, np.ndarray] data and PlotSpec configuration, following
the v1.0.0 architecture design.
"""

from typing import Dict, List, Optional, Any, Union
import numpy as np
import plotly.graph_objects as go

from .plotspec import PlotSpec


def plot(data: Dict[str, np.ndarray], spec: PlotSpec) -> go.Figure:
    """
    Create Plotly figure from data and PlotSpec configuration.
    
    Args:
        data: Signal name → numpy array mapping
        spec: PlotSpec configuration object
        
    Returns:
        Plotly Figure object
        
    Raises:
        ValueError: If required signals are missing from data
    """
    # Convert PlotSpec to config dict
    config = spec.to_dict()
    
    # Create figure and apply layout
    fig = create_figure()
    layout = create_layout(config)
    fig.update_layout(layout)
    
    # Get X-axis data
    x_signal = config["x"]
    if x_signal not in data:
        raise ValueError(f"X-axis signal '{x_signal}' not found in data. Available: {list(data.keys())}")
    x_data = data[x_signal]
    
    # Add traces for each Y-axis
    for y_axis_idx, y_spec in enumerate(config["y"]):
        # Determine Y-axis ID
        y_axis_id = "y" if y_axis_idx == 0 else f"y{y_axis_idx + 1}"
        
        # Add each signal in this Y-axis
        for legend_name, signal_key in y_spec["signals"].items():
            if signal_key not in data:
                raise ValueError(f"Signal '{signal_key}' not found in data. Available: {list(data.keys())}")
            
            y_data = data[signal_key]
            add_waveform(fig, x_data, y_data, name=legend_name, y_axis=y_axis_id)
    
    return fig


def create_figure() -> go.Figure:
    """
    Create empty Plotly figure with basic setup.
    
    Returns:
        Empty Plotly Figure object
    """
    return go.Figure()


def create_layout(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create layout configuration for Plotly figure.
    
    Args:
        config: Configuration dictionary from PlotSpec.to_dict()
        
    Returns:
        Layout configuration dictionary
    """
    layout = {}
    
    # Title configuration
    if config.get("title"):
        layout["title"] = {
            "text": config["title"],
            "x": config.get("title_x", 0.5),
            "xanchor": config.get("title_xanchor", "center")
        }
    
    # Figure dimensions
    if config.get("width"):
        layout["width"] = config["width"]
    if config.get("height"):
        layout["height"] = config["height"]
    
    # Theme
    if config.get("theme") and config["theme"] != "plotly":
        layout["template"] = config["theme"]
    
    # Legend
    layout["showlegend"] = config.get("show_legend", True)
    
    # X-axis configuration
    layout["xaxis"] = {
        "title": config.get("x", "X-axis"),
        "showgrid": config.get("grid", True),
        "rangeslider": {"visible": config.get("show_rangeslider", True)}
    }
    
    # Y-axes configuration
    num_y_axes = len(config.get("y", []))
    
    if num_y_axes > 0:
        # Calculate Y-axis domains for multi-axis plots
        if num_y_axes == 1:
            # Single Y-axis gets full domain
            domains = [[0, 1]]
        else:
            # Multiple Y-axes share the space
            gap = 0.05
            total_gap_space = gap * (num_y_axes - 1)
            effective_height = 1.0 - total_gap_space
            single_axis_height = effective_height / num_y_axes
            
            domains = []
            current_bottom = 0
            for i in range(num_y_axes):
                domain_top = current_bottom + single_axis_height
                domains.append([current_bottom, domain_top])
                current_bottom = domain_top + gap
        
        # Configure each Y-axis
        for i, y_spec in enumerate(config["y"]):
            axis_key = "yaxis" if i == 0 else f"yaxis{i + 1}"
            
            axis_config = {
                "title": y_spec.get("label", f"Y-axis {i + 1}"),
                "showgrid": config.get("grid", True),
                "domain": domains[i],
                "anchor": "x"
            }
            
            # Log scale support
            if y_spec.get("log_scale", False):
                axis_config["type"] = "log"
            
            # Range support
            if y_spec.get("range"):
                axis_config["range"] = y_spec["range"]
            
            layout[axis_key] = axis_config
    
    # Zoom buttons configuration
    if config.get("zoom_buttons", False) and num_y_axes > 0:
        # Create Y-axis identifiers for zoom button configuration
        y_axis_ids = []
        for i in range(num_y_axes):
            axis_id = "yaxis" if i == 0 else f"yaxis{i + 1}"
            y_axis_ids.append(axis_id)
        
        # Zoom XY (both X and Y axes free)
        xy_zoom_args = {"dragmode": "zoom", "xaxis.fixedrange": False}
        for axis_id in y_axis_ids:
            xy_zoom_args[f"{axis_id}.fixedrange"] = False
        
        zoom_buttons = [
            dict(label="Zoom XY", method="relayout", args=[xy_zoom_args])
        ]
        
        # Zoom Y (all Y axes, X fixed)
        y_zoom_args = {"dragmode": "zoom", "xaxis.fixedrange": True}
        for axis_id in y_axis_ids:
            y_zoom_args[f"{axis_id}.fixedrange"] = False
        zoom_buttons.append(dict(label="Zoom Y", method="relayout", args=[y_zoom_args]))
        
        # Zoom X (X axis, Y axes fixed)
        x_zoom_args = {"dragmode": "zoom", "xaxis.fixedrange": False}
        for axis_id in y_axis_ids:
            x_zoom_args[f"{axis_id}.fixedrange"] = True
        zoom_buttons.append(dict(label="Zoom X", method="relayout", args=[x_zoom_args]))
        
        layout["updatemenus"] = [
            dict(
                type="buttons",
                direction="right",
                x=config.get("zoom_buttons_x", 0.05), 
                xanchor="left",
                y=config.get("zoom_buttons_y", 1.05), 
                yanchor="bottom",
                showactive=True,
                buttons=zoom_buttons
            )
        ]
    
    return layout


def add_waveform(fig: go.Figure, x_data: np.ndarray, y_data: np.ndarray, 
                name: str, y_axis: str = "y", **kwargs) -> None:
    """
    Add single waveform trace to figure.
    
    Args:
        fig: Plotly figure to add trace to
        x_data: X-axis data array
        y_data: Y-axis data array
        name: Trace name for legend
        y_axis: Y-axis identifier (y, y2, y3, etc.)
        **kwargs: Additional trace styling options
    """
    # Create scatter trace
    trace = go.Scatter(
        x=x_data,
        y=y_data,
        name=name,
        yaxis=y_axis,
        **kwargs
    )
    
    # Add trace to figure
    fig.add_trace(trace) 