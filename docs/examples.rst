Examples
========

.. note::
   All code below targets *wave_view* **1.0.0**.  The modern workflow is:

   1. ``data, _ = wv.load_spice_raw("my.raw")`` – obtain a ``dict`` of NumPy arrays
   2. ``spec = wv.PlotSpec.from_yaml(""" ... """)`` – build a PlotSpec (YAML string or file)
   3. ``fig = wv.plot(data, spec)`` – create the Plotly figure

   Legacy helpers such as ``config_from_yaml`` were removed.

This page contains practical examples for common use cases with wave_view.

Basic Voltage Plot
------------------

Plot input and output voltages from an amplifier simulation:

.. code-block:: python

   import wave_view as wv

   # Load simulation data
   data, _ = wv.load_spice_raw("amplifier.raw")

   # Simple voltage plot using YAML configuration
   spec = wv.PlotSpec.from_yaml("""
   title: "Amplifier Response"
   x: "time"
   y:
     - label: "Voltage (V)"
       signals:
         Input: "v(in)"
         Output: "v(out)"
   """)

   fig = wv.plot(data, spec)
   fig.show()

Current Analysis
----------------

Analyze transistor currents with logarithmic scale:

.. code-block:: python

   data, _ = wv.load_spice_raw("transistor_analysis.raw")

   spec = wv.PlotSpec.from_yaml("""
   title: "Transistor Current Analysis"
   x: "time"
   y:
     - label: "Current (A)"
       log_scale: true
       signals:
         M1: "i(m1)"
         M2: "i(m2)"
         M3: "i(m3)"
   """)

   fig = wv.plot(data, spec)

Multi-Plot Analysis
-------------------

Create multiple subplots for comprehensive analysis:

.. code-block:: python

   data, _ = wv.load_spice_raw("complete_analysis.raw")

   spec = wv.PlotSpec.from_yaml("""
   title: "Complete Circuit Analysis"
   x: "time"
   y:
     - label: "Voltage (V)"
       signals:
         Input: "v(in)"
         Output: "v(out)"
     - label: "Current (A)"
       log_scale: true
       signals:
         M1: "i(m1)"
         M2: "i(m2)"
     - label: "Supply Voltage (V)"
       signals:
         VDD: "v(vdd)"
         VSS: "v(vss)"
   """)

   fig = wv.plot(data, spec)

Power Analysis with Processed Data
-----------------------------------

Combine SPICE signals with computed power calculations:

.. code-block:: python

   import numpy as np
   import wave_view as wv

   # Load SPICE data
   data, _ = wv.load_spice_raw("power_analysis.raw")
   
   # Compute power signals
   v_out = data["v(out)"]
   i_out = data["i(rload)"]
   power = v_out * i_out
   
   # Create processed data dictionary
   processed_signals = {
       "power_output": power,
       "power_avg": np.ones_like(power) * np.mean(power)
   }

   # Merge derived signals into the main data dictionary
   data.update(processed_signals)

   spec = wv.PlotSpec.from_yaml("""
   title: "Power Analysis"
   x: "time"
   y:
     - label: "Voltage (V)"
       signals:
         Output: "v(out)"
     - label: "Power (W)"
       signals:
         Output_Power: "power_output"
         Average_Power: "power_avg"
   """)

   fig = wv.plot(data, spec)

AC Analysis with Complex Signal Processing
--------------------------------------------

AC analysis results contain complex numbers for voltage and current signals, enabling proper 
magnitude and phase analysis for transfer functions and Bode plots:

.. code-block:: python

   import wave_view as wv
   import numpy as np

   # Load AC analysis data (contains complex numbers)
   data_ac, _ = wv.load_spice_raw("ac_analysis.raw")
   
   # AC signals are automatically returned as complex numbers
   frequency = data_ac["frequency"]  # Real (even though stored as complex)
   v_out = data_ac["v(out)"]         # Complex
   v_in = data_ac["v(in)"]    # complex128 array
   
   print(f"v_out dtype: {v_out.dtype}")  # complex128
   print(f"Is complex: {np.iscomplexobj(v_out)}")  # True

**Basic AC Magnitude Plot:**

.. code-block:: python

   # Simple magnitude plot (uses real part of complex signal)
   spec = wv.PlotSpec.from_yaml("""
   title: "AC Magnitude Response"
   x: "frequency"
   y:
     - label: "Voltage (V)"
       signals:
         Output: "v(out)"  # Automatically uses real part
   """)

   fig = wv.plot(data_ac, spec)

**Complete Bode Plot (Magnitude and Phase):**

.. code-block:: python

   # Process complex signals for magnitude and phase analysis
   processed_data = {
       "magnitude_db": 20 * np.log10(np.abs(v_out)),      # Magnitude in dB
       "phase_deg": np.angle(v_out) * 180 / np.pi,        # Phase in degrees
       "magnitude_linear": np.abs(v_out),                  # Linear magnitude
       "phase_rad": np.angle(v_out)                        # Phase in radians
   }

   spec = wv.PlotSpec.from_yaml("""
   title: "Transfer Function Bode Plot"
   x: "frequency"
   y:
     - label: "Magnitude (dB)"
       signals:
         H(jω): "magnitude_db"
     - label: "Phase (degrees)"
       signals:
         φ(jω): "phase_deg"
   height: 800
   zoom_buttons: true
   show_rangeslider: true
   """)

   data_ac2, _ = wv.load_spice_raw("ac_analysis.raw")
   # Merge processed values into data dictionary before plotting
   data_ac2.update(processed_data)
   fig = wv.plot(data_ac2, spec)

**Transfer Function Analysis:**

.. code-block:: python

   # Calculate transfer function H(jω) = V_out / V_in
   transfer_function = v_out / v_in
   
   # Process for comprehensive analysis
   processed_data = {
       "tf_magnitude_db": 20 * np.log10(np.abs(transfer_function)),
       "tf_phase_deg": np.angle(transfer_function) * 180 / np.pi,
       "input_magnitude_db": 20 * np.log10(np.abs(v_in)),
       "output_magnitude_db": 20 * np.log10(np.abs(v_out))
   }

   spec = wv.PlotSpec.from_yaml("""
   title: "Complete Transfer Function Analysis"
   x: "frequency"
   y:
     - label: "Transfer Function Magnitude (dB)"
       signals:
         "|H(jω)|": "tf_magnitude_db"
     - label: "Transfer Function Phase (°)"
       signals:
         "∠H(jω)": "tf_phase_deg"
     - label: "Input/Output Magnitude (dB)"
       signals:
         Input: "input_magnitude_db"
         Output: "output_magnitude_db"
   height: 900
   """)

   data_ac3, _ = wv.load_spice_raw("ac_analysis.raw")
   data_ac3.update(processed_data)
   fig = wv.plot(data_ac3, spec)

**Working with Complex Numbers:**

.. code-block:: python

   # AC analysis preserves complex numbers for calculations
   frequency = data_ac["frequency"]  # Real (even though stored as complex)
   v_out = data_ac["v(out)"]         # Complex
   
   # Extract components
   real_part = np.real(v_out)
   imag_part = np.imag(v_out)
   magnitude = np.abs(v_out)
   phase_rad = np.angle(v_out)
   
   # Complex signal analysis
   processed_data = {
       "real_component": real_part,
       "imaginary_component": imag_part,
       "magnitude": magnitude,
       "phase_unwrapped": np.unwrap(phase_rad) * 180 / np.pi  # Unwrap phase
   }

   spec = wv.PlotSpec.from_yaml("""
   title: "Complex Signal Components"
   x: "frequency"
   y:
     - label: "Real/Imaginary Parts"
       signals:
         Real: "real_component"
         Imaginary: "imaginary_component"
     - label: "Magnitude"
       signals:
         "|V|": "magnitude"
     - label: "Unwrapped Phase (°)"
       signals:
         "φ": "phase_unwrapped"
   """)

   fig = wv.plot(data_ac, spec)

.. note::
   
   **Complex Number Handling:**
   
   - Raw AC signals are preserved as complex numbers (``complex128``)
   - Use ``np.abs()`` for magnitude and ``np.angle()`` for phase
   - Frequency and time signals are automatically converted to real numbers
   - Raw signals in plots automatically use the real part for display
   - Add magnitude/phase arrays to the *data* dictionary before plotting

YAML Configuration File
-----------------------

For complex configurations, use YAML files:

.. code-block:: yaml

   # analysis_config.yaml
   title: "Operational Amplifier Analysis"
   x: "time"
   y:
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
   spec = wv.PlotSpec.from_file("analysis_config.yaml")
   data, _ = wv.load_spice_raw("opamp.raw")
   fig = wv.plot(data, spec)

Batch Processing
----------------

Process multiple simulation files with the same configuration:

.. code-block:: python

   import wave_view as wv
   from pathlib import Path

   # Common configuration for all simulations
   spec = wv.PlotSpec.from_yaml("""
   title: "Output Voltage Analysis"
   x: "time"
   y:
     - label: "Voltage (V)"
       signals:
         Output: "v(out)"
   """)

   # Process all .raw files in a directory
   raw_files = Path("simulations").glob("*.raw")
   
   for raw_file in raw_files:
       data_i, _ = wv.load_spice_raw(raw_file)
       fig = wv.plot(data_i, spec)
       
       # Save with descriptive name
       output_name = f"{raw_file.stem}_plot.html"
       fig.write_html(output_name)
       print(f"Created {output_name}")

Interactive Exploration
-----------------------

Discover available signals by loading the data and printing the keys:

.. code-block:: python

   import wave_view as wv

   data, _ = wv.load_spice_raw("mystery_circuit.raw")
   print(list(data))

Error Handling
--------------

Robust error handling for production use:

.. code-block:: python

   import wave_view as wv

   def safe_plot(raw_file, spec):
       """Safely plot with error handling."""
       try:
           # Try to create plot
           data_i, _ = wv.load_spice_raw(raw_file)
           fig = wv.plot(data_i, spec)
           return fig
           
       except FileNotFoundError:
           print(f"File not found: {raw_file}")
       except Exception as e:
           print(f"Plotting error: {e}")
       
       return None

   # Usage
   spec = wv.PlotSpec.from_yaml("""
   x: "time"
   y:
     - signals:
         OUT: "v(out)"
   """)
   fig = safe_plot("simulation.raw", spec)
   
   if fig:
       fig.show()

Comparison Plots
----------------

Compare results from different simulation runs:

.. code-block:: python

   # Load multiple simulations
   data1, _ = wv.load_spice_raw("before_optimization.raw")
   data2, _ = wv.load_spice_raw("after_optimization.raw")

   # Create comparison signals
   processed_signals = {
       "v_out_before": data1["v(out)"],
       "v_out_after": data2["v(out)"]
   }

   # Merge into base dictionary (time base from first simulation)
   data1.update(processed_signals)

   spec = wv.PlotSpec.from_yaml("""
   title: "Optimization Comparison"
   x: "time"
   y:
     - label: "Voltage (V)"
       signals:
         Before: "v_out_before"
         After: "v_out_after"
   """)

   fig = wv.plot(data1, spec) 