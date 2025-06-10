Examples
========

This page contains practical examples for common use cases with wave_view.

Basic Voltage Plot
------------------

Plot input and output voltages from an amplifier simulation:

.. code-block:: python

   import wave_view as wv

   # Simple voltage plot
   config = {
       "title": "Amplifier Response",
       "plots": [
           {
               "signals": ["v(in)", "v(out)"],
               "title": "Input vs Output Voltage",
               "ylabel": "Voltage (V)"
           }
       ]
   }

   fig = wv.plot("amplifier.raw", config)
   fig.show()

Current Analysis
----------------

Analyze transistor currents with logarithmic scale:

.. code-block:: python

   config = {
       "title": "Transistor Current Analysis",
       "plots": [
           {
               "signals": ["i(m1)", "i(m2)", "i(m3)"],
               "title": "MOSFET Currents",
               "ylabel": "Current (A)",
               "log_y": True
           }
       ]
   }

   fig = wv.plot("transistor_analysis.raw", config)

Multi-Plot Analysis
-------------------

Create multiple subplots for comprehensive analysis:

.. code-block:: python

   config = {
       "title": "Complete Circuit Analysis",
       "plots": [
           {
               "signals": ["v(in)", "v(out)"],
               "title": "Voltage Waveforms",
               "ylabel": "Voltage (V)"
           },
           {
               "signals": ["i(m1)", "i(m2)"],
               "title": "Current Consumption",
               "ylabel": "Current (A)",
               "log_y": True
           },
           {
               "signals": ["v(vdd)", "v(vss)"],
               "title": "Supply Rails",
               "ylabel": "Supply Voltage (V)"
           }
       ]
   }

   fig = wv.plot("complete_analysis.raw", config)

Power Analysis with Processed Data
-----------------------------------

Combine SPICE signals with computed power calculations:

.. code-block:: python

   import numpy as np
   import wave_view as wv

   # Load SPICE data
   spice_data = wv.load_spice("power_analysis.raw")
   
   # Compute power signals
   v_out = spice_data.get_signal_data("v(out)")
   i_out = spice_data.get_signal_data("i(rload)")
   power = v_out * i_out
   
   # Create processed data dictionary
   processed_signals = {
       "power_output": power,
       "power_avg": np.ones_like(power) * np.mean(power)
   }

   config = {
       "title": "Power Analysis",
       "plots": [
           {
               "signals": ["v(out)"],
               "title": "Output Voltage",
               "ylabel": "Voltage (V)"
           },
           {
               "signals": ["power_output", "power_avg"],
               "title": "Output Power",
               "ylabel": "Power (W)"
           }
       ]
   }

   fig = wv.plot("power_analysis.raw", config, processed_data=processed_signals)

AC Analysis
-----------

Plot frequency response from AC analysis:

.. code-block:: python

   config = {
       "title": "Frequency Response",
       "plots": [
           {
               "signals": ["v(out)"],
               "title": "Magnitude Response",
               "xlabel": "Frequency (Hz)",
               "ylabel": "Magnitude (dB)",
               "log_x": True
           }
       ]
   }

   fig = wv.plot("ac_analysis.raw", config)

YAML Configuration File
-----------------------

For complex configurations, use YAML files:

.. code-block:: yaml

   # analysis_config.yaml
   title: "Operational Amplifier Analysis"
   plots:
     - signals: ["v(inp)", "v(inn)", "v(out)"]
       title: "Input and Output Signals"
       ylabel: "Voltage (V)"
       
     - signals: ["i(m1)", "i(m2)", "i(m3)", "i(m4)"]
       title: "Transistor Currents"
       ylabel: "Current (A)"
       log_y: true
       
     - signals: ["v(vdd)", "v(vss)"]
       title: "Power Supply"
       ylabel: "Supply Voltage (V)"
       grid: false

.. code-block:: python

   import wave_view as wv

   # Load configuration from file
   config = wv.config_from_file("analysis_config.yaml")
   fig = wv.plot("opamp.raw", config)

Batch Processing
----------------

Process multiple simulation files with the same configuration:

.. code-block:: python

   import wave_view as wv
   from pathlib import Path

   # Common configuration for all simulations
   config = {
       "plots": [
           {
               "signals": ["v(out)"],
               "title": "Output Voltage",
               "ylabel": "Voltage (V)"
           }
       ]
   }

   # Process all .raw files in a directory
   raw_files = Path("simulations").glob("*.raw")
   
   for raw_file in raw_files:
       fig = wv.plot(raw_file, config)
       
       # Save with descriptive name
       output_name = f"{raw_file.stem}_plot.html"
       fig.write_html(output_name)
       print(f"Created {output_name}")

Interactive Exploration
-----------------------

Use explore_signals to discover what's available:

.. code-block:: python

   import wave_view as wv

   # Discover available signals
   signals = wv.explore_signals("mystery_circuit.raw")
   
   print("Voltage signals:", signals['voltage_signals'])
   print("Current signals:", signals['current_signals'])
   print("Other signals:", signals['other_signals'])

   # Create configuration based on discovery
   config = {
       "plots": [
           {
               "signals": signals['voltage_signals'][:3],  # First 3 voltage signals
               "title": "Main Voltages"
           },
           {
               "signals": signals['current_signals'][:2],  # First 2 current signals
               "title": "Main Currents",
               "log_y": True
           }
       ]
   }

   fig = wv.plot("mystery_circuit.raw", config)

Error Handling
--------------

Robust error handling for production use:

.. code-block:: python

   import wave_view as wv

   def safe_plot(raw_file, config):
       """Safely plot with error handling."""
       try:
           # Validate configuration first
           errors = wv.validate_config(config)
           if errors:
               print(f"Configuration errors: {errors}")
               return None
           
           # Try to create plot
           fig = wv.plot(raw_file, config)
           return fig
           
       except FileNotFoundError:
           print(f"File not found: {raw_file}")
       except Exception as e:
           print(f"Plotting error: {e}")
       
       return None

   # Usage
   config = {"plots": [{"signals": ["v(out)"]}]}
   fig = safe_plot("simulation.raw", config)
   
   if fig:
       fig.show()

Comparison Plots
----------------

Compare results from different simulation runs:

.. code-block:: python

   # Load multiple simulations
   data1 = wv.load_spice("before_optimization.raw")
   data2 = wv.load_spice("after_optimization.raw")

   # Create comparison signals
   processed_signals = {
       "v_out_before": data1.get_signal_data("v(out)"),
       "v_out_after": data2.get_signal_data("v(out)")
   }

   config = {
       "title": "Optimization Comparison",
       "plots": [
           {
               "signals": ["v_out_before", "v_out_after"],
               "title": "Output Voltage Comparison",
               "ylabel": "Voltage (V)"
           }
       ]
   }

   # Use time base from first simulation
   fig = wv.plot("before_optimization.raw", config, processed_data=processed_signals) 