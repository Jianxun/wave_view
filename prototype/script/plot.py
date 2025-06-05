from spicelib import RawRead # Assuming spicelib is installed and in the Python path
import numpy as np # Import numpy for NumPy arrays
import sys # Import sys for sys.exit
import os # Import for path manipulation

import plotly.graph_objects as go
import numpy as np
import yaml # For loading plot_config.yaml
import plotly.io as pio

def create_plotly_figure(
    plot_config: dict,
    raw_data_obj,
    processed_data: dict[str, np.ndarray] = None
) -> go.Figure:
    """
    Creates a Plotly figure based on plot_config, raw SPICE data, and optional processed data.

    Args:
        plot_config: Dictionary defining the plot structure, labels, and
                     signal keys (e.g., "raw.v(vdd)", "data.my_signal").
        raw_data_obj: The object from spicelib.RawRead() containing simulation data.
                      Required if any signal_key uses the "raw." prefix.
        processed_data: A dictionary where keys are identifiers for processed signals
                        (e.g., "my_signal") and values are NumPy arrays. Used when a
                        signal_key has the "data." prefix. Defaults to an empty dict if None.

    Returns:
        A plotly.graph_objects.Figure object.
    """
    if processed_data is None:
        processed_data = {}

    def _get_signal_data(signal_key_str: str) -> np.ndarray:
        if not isinstance(signal_key_str, str):
            raise TypeError(f"Signal key must be a string, got {type(signal_key_str)}: {signal_key_str}")

        if signal_key_str.startswith("data."):
            data_dict_key = signal_key_str[5:] # Remove "data."
            if data_dict_key not in processed_data:
                raise ValueError(
                    f"Key '{data_dict_key}' not found in 'processed_data' dictionary for signal key '{signal_key_str}'."
                )
            return np.array(processed_data[data_dict_key], dtype=float) # Ensure float
        else: # Default to raw signal or explicit raw.
            if raw_data_obj is None:
                raise ValueError(
                    f"Signal key '{signal_key_str}' requires raw_data_obj (as it's not a 'data.' prefixed signal), but raw_data_obj was not provided."
                )
            
            trace_name = signal_key_str
            if signal_key_str.startswith("raw."):
                trace_name = signal_key_str[4:] # Remove "raw."
            
            trace = raw_data_obj.get_trace(trace_name)
            if trace is None:
                raise ValueError(f"Trace '{trace_name}' (derived from signal key '{signal_key_str}') not found in raw_data_obj.")
            return np.array(trace, dtype=float) # Ensure float for plotting

    fig = go.Figure()

    # Get X-axis data
    x_config = plot_config.get("X")
    if not x_config or not isinstance(x_config.get("signal_key"), str):
        raise ValueError("X-axis 'signal_key' must be specified in plot_config.")
    x_data = _get_signal_data(x_config["signal_key"])
    x_axis_title = x_config.get("label", x_config["signal_key"])


    # Prepare Y-axes
    y_axes_config = plot_config.get("Y", [])
    num_y_axes = len(y_axes_config)
    if num_y_axes == 0:
        print("Warning: No Y defined in plot_config.")
        # Potentially return an empty figure or raise error, for now, it will be an empty plot
    
    y_axis_domains = []
    if num_y_axes > 0:
        gap = 0.05 # Gap between y-axes (e.g., 5% of total height)
        total_gap_space = gap * (num_y_axes - 1) if num_y_axes > 1 else 0
        effective_plot_height = 1.0 - total_gap_space
        single_axis_height = effective_plot_height / num_y_axes

        current_bottom = 0
        for i in range(num_y_axes):
            domain_top = current_bottom + single_axis_height
            y_axis_domains.append([current_bottom, domain_top])
            current_bottom = domain_top + gap
    y_axis_domains.reverse() # Plotly lays out from bottom to top, config is often top to bottom

    layout_update_dict = {}
    plotly_y_axis_ids = [] # To keep track of yaxis, yaxis2, etc. for zoom buttons

    for i, y_axis_cfg in enumerate(y_axes_config):
        plotly_axis_id_num = i + 1
        plotly_axis_id_str = f"yaxis{plotly_axis_id_num if plotly_axis_id_num > 1 else ''}" # 'yaxis', 'yaxis2', ...
        plotly_y_axis_ids.append(plotly_axis_id_str)

        axis_layout_key = f"yaxis{plotly_axis_id_num}" # Key for layout update (e.g. 'yaxis', 'yaxis2')

        layout_update_dict[axis_layout_key] = {
            "title": y_axis_cfg.get("label", f"Y-Axis {plotly_axis_id_num}"),
            "domain": y_axis_domains[i],
        }
        if i > 0: # Anchor subsequent axes to the main x-axis
             layout_update_dict[axis_layout_key]["anchor"] = "x"


        for legend_name, signal_key_val in y_axis_cfg.get("signals", {}).items():
            y_data_for_trace = _get_signal_data(signal_key_val)
            fig.add_trace(go.Scatter(
                x=x_data,
                y=y_data_for_trace,
                name=legend_name,
                yaxis=f"y{plotly_axis_id_num}" # Associate with yaxis, yaxis2 etc.
            ))

    # Global layout settings
    layout_update_dict["title_text"] = plot_config.get("title", "Spice Waveform Plot")
    layout_update_dict["height"] = plot_config.get("plot_height", 600 if num_y_axes <= 1 else 300 * num_y_axes)
    layout_update_dict["dragmode"] = plot_config.get("default_dragmode", "zoom")
    
    layout_update_dict["xaxis"] = {
        "title": x_axis_title,
        "rangeslider": {"visible": plot_config.get("show_rangeslider", True)},
        "domain": [0,1] # X-axis spans the full width
    }
    
    # Configure zoom buttons
    if plot_config.get("show_zoom_buttons", True) and num_y_axes > 0:
        zoom_buttons = [
            dict(label="Zoom XY", method="relayout", args=[{"dragmode": "zoom"}]) # Default, all axes zoomable
        ]
        
        # Zoom Y (all Y axes, X fixed)
        y_zoom_args = {"dragmode": "zoom", "xaxis.fixedrange": True}
        for axis_id_str in plotly_y_axis_ids:
            y_zoom_args[f"{axis_id_str}.fixedrange"] = False
        zoom_buttons.append(dict(label="Zoom Y", method="relayout", args=[y_zoom_args]))

        # Zoom X (all X axes, Ys fixed)
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
    
    fig.update_layout(**layout_update_dict)
    return fig

# Example usage (to be adapted by the user)
if __name__ == "__main__":
    # This is an example. Users should adapt this to their specific file paths and data.
    
    # Configure Plotly to open in browser
    pio.renderers.default = "browser"
    
    # 1. Define path to your plot configuration YAML file
    plot_config_path = "./plot_config.yaml" # Make sure this file exists

    # Create an example plot_config.yaml if it doesn't exist for demonstration
    example_yaml_content = """title: "Example SPICE Waveform Plot"
source: "./your_simulation.raw"  # Path to your .raw file relative to this config file

X:
  label: "Time (s)"
  signal_key: "raw.time"  # Use time from the raw file

Y:
  - label: "Voltage (V)"
    signals:
      VDD: "v(vdd)"      # Plot VDD voltage
      VSS: "v(vss)"      # Plot VSS voltage
  - label: "Current (A)"
    signals:
      IDD: "i(vdd)"      # Plot VDD current on separate Y-axis

# Optional settings:
plot_height: 600
show_rangeslider: true
show_zoom_buttons: true
default_dragmode: "zoom"
"""
    try:
        with open(plot_config_path, 'r') as f:
            yaml.safe_load(f) # Try to load it
    except FileNotFoundError:
        print(f"Example plot_config.yaml not found at {plot_config_path}. Creating a sample one.")
        print("Please REVIEW and EDIT this sample to match your .raw file and desired plots.")
        with open(plot_config_path, 'w') as f:
            f.write(example_yaml_content)
        print(f"Sample {plot_config_path} created. Please edit it and re-run.")
        sys.exit(0)  # Exit after creating the template
       

    try:
        # 2. Load plot configuration from YAML
        with open(plot_config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        # Determine the directory of the plot_config.yaml file
        config_dir = os.path.dirname(os.path.abspath(plot_config_path))
        
        # Get the relative raw file path from the config
        relative_raw_path = config.get("source")
        if not relative_raw_path:
            raise ValueError("The 'source' key for the raw file path is missing in plot_config.yaml.")
            
        # Construct the absolute path to the raw file
        raw_file_actual_path = os.path.join(config_dir, relative_raw_path)
        raw_file_actual_path = os.path.normpath(raw_file_actual_path) # Normalize the path (e.g., remove ./)


        # 3. Load raw SPICE data
        spice_data = RawRead(raw_file_actual_path)
        print(f"Successfully loaded {raw_file_actual_path}")
        
        # Print available traces for user convenience (optional)
        available_traces = spice_data.get_trace_names()
        print("\nAvailable traces in raw file:")
        for trace_name in available_traces:
            print(f"- {trace_name}")
        print("\n")


        # 4. Prepare any processed data (as defined in your plot_config.yaml under "data.")
        my_processed_data = {}
        
        # Example: if plot_config.yaml uses "data.inverted_id_vd1"
        # This checks if the key "inverted_id_vd1" is expected by any trace in the config.
        # A more robust way would be to parse config to see what data.* keys are needed.
        # For now, we will try to create it if i(vd1) exists.
        
        # Check if "data.inverted_id_vd1" is used in the config
        needs_inverted_id_vd1 = False
        for y_axis in config.get("Y", []):
            for signal_key in y_axis.get("signals", {}).values():
                if signal_key == "data.inverted_id_vd1":
                    needs_inverted_id_vd1 = True
                    break
            if needs_inverted_id_vd1:
                break
        
        if needs_inverted_id_vd1:
            if "i(vd1)" in available_traces:
                raw_id_vd1 = np.array(spice_data.get_trace("i(vd1)"), dtype=float)
                my_processed_data["inverted_id_vd1"] = -1 * raw_id_vd1
                print("Processed 'inverted_id_vd1' for plotting.")
            else:
                print("Warning: 'i(vd1)' not found in raw file, cannot create 'data.inverted_id_vd1'.")


        # 5. Create the figure
        fig = create_plotly_figure(
            plot_config=config,
            raw_data_obj=spice_data,
            processed_data=my_processed_data
        )

        # 6. Show the figure
        print("Opening plot in browser...")
        fig.show()
        print("Plot should now be displayed in your default browser.")

    except FileNotFoundError as e:
        print(f"Error: Could not find a required file: {e.filename}")
        if "plot_config.yaml" in str(e.filename):
            print(f"Please ensure '{plot_config_path}' exists and is correctly formatted.")
        elif ".raw" in str(e.filename):
             print(f"Please ensure the raw file specified in '{plot_config_path}' (key: 'source') exists at that path.")
    except ImportError:
        print("Error: PyYAML is not installed. Please install it by running: pip install PyYAML")
    except Exception as e:
        print(f"An error occurred during plot generation: {e}")
        import traceback
        traceback.print_exc()
