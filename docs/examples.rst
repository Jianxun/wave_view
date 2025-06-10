Examples
========

This page contains practical examples for common use cases with wave_view.

Basic Voltage Plot
------------------

Plot input and output voltages from an amplifier simulation:

.. code-block:: python

   import wave_view as wv

   # Simple voltage plot using YAML configuration
   config = wv.config_from_yaml("""
   title: "Amplifier Response"
   X:
     signal_key: "time"
     label: "Time (s)"
   Y:
     - label: "Voltage (V)"
       signals:
         Input: "v(in)"
         Output: "v(out)"
   """)

   fig = wv.plot("amplifier.raw", config)
   fig.show()

Current Analysis
----------------

Analyze transistor currents with logarithmic scale:

.. code-block:: python

   config = wv.config_from_yaml("""
   title: "Transistor Current Analysis"
   X:
     signal_key: "time"
     label: "Time (s)"
   Y:
     - label: "Current (A)"
       scale: "log"
       signals:
         M1: "i(m1)"
         M2: "i(m2)"
         M3: "i(m3)"
   """)

   fig = wv.plot("transistor_analysis.raw", config)

Multi-Plot Analysis
-------------------

Create multiple subplots for comprehensive analysis:

.. code-block:: python

   config = wv.config_from_yaml("""
   title: "Complete Circuit Analysis"
   X:
     signal_key: "time"
     label: "Time (s)"
   Y:
     - label: "Voltage (V)"
       signals:
         Input: "v(in)"
         Output: "v(out)"
     - label: "Current (A)"
       scale: "log"
       signals:
         M1: "i(m1)"
         M2: "i(m2)"
     - label: "Supply Voltage (V)"
       signals:
         VDD: "v(vdd)"
         VSS: "v(vss)"
   """)

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

   config = wv.config_from_yaml("""
   title: "Power Analysis"
   X:
     signal_key: "time"
     label: "Time (s)"
   Y:
     - label: "Voltage (V)"
       signals:
         Output: "v(out)"
     - label: "Power (W)"
       signals:
         Output_Power: "data.power_output"
         Average_Power: "data.power_avg"
   """)

   fig = wv.plot("power_analysis.raw", config, processed_data=processed_signals)

AC Analysis
-----------

Plot frequency response from AC analysis:

.. code-block:: python

   config = wv.config_from_yaml("""
   title: "Frequency Response"
   X:
     signal_key: "frequency"
     label: "Frequency (Hz)"
     scale: "log"
   Y:
     - label: "Magnitude (dB)"
       signals:
         Output: "v(out)"
   """)

   fig = wv.plot("ac_analysis.raw", config)

YAML Configuration File
-----------------------

For complex configurations, use YAML files:

.. code-block:: yaml

   # analysis_config.yaml
   title: "Operational Amplifier Analysis"
   X:
     signal_key: "time"
     label: "Time (s)"
   Y:
     - label: "Voltage (V)"
       signals:
         Input_P: "v(inp)"
         Input_N: "v(inn)"
         Output: "v(out)"
     - label: "Current (A)"
       scale: "log"
       signals:
         M1: "i(m1)"
         M2: "i(m2)"
         M3: "i(m3)"
         M4: "i(m4)"
     - label: "Supply Voltage (V)"
       signals:
         VDD: "v(vdd)"
         VSS: "v(vss)"

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
   config = wv.config_from_yaml("""
   title: "Output Voltage Analysis"
   X:
     signal_key: "time"
     label: "Time (s)"
   Y:
     - label: "Voltage (V)"
       signals:
         Output: "v(out)"
   """)

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
   voltage_signals = {f"V{i+1}": sig for i, sig in enumerate(signals['voltage_signals'][:3])}
   current_signals = {f"I{i+1}": sig for i, sig in enumerate(signals['current_signals'][:2])}
   
   config = wv.config_from_yaml(f"""
   title: "Discovered Signals Analysis"
   X:
     signal_key: "time"
     label: "Time (s)"
   Y:
     - label: "Main Voltages (V)"
       signals: {voltage_signals}
     - label: "Main Currents (A)"
       scale: "log"
       signals: {current_signals}
   """)

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
   config = wv.config_from_yaml("""
   X:
     signal_key: "time"
   Y:
     - signals:
         OUT: "v(out)"
   """)
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

   config = wv.config_from_yaml("""
   title: "Optimization Comparison"
   X:
     signal_key: "time"
     label: "Time (s)"
   Y:
     - label: "Voltage (V)"
       signals:
         Before: "data.v_out_before"
         After: "data.v_out_after"
   """)

   # Use time base from first simulation
   fig = wv.plot("before_optimization.raw", config, processed_data=processed_signals) 