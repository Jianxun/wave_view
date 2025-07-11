Examples
========

.. note::
   All code below targets *wave_view* **1.0.0**.  The modern workflow is:

   1. ``data, metadata = wv.load_spice_raw("my.raw")`` – obtain a ``dict`` of NumPy arrays, and a ``dict`` of metadata (placeholders for future features)
   2. ``spec = wv.PlotSpec.from_yaml(""" ... """)`` – build a PlotSpec (YAML string or file)
   3. ``fig = wv.plot(data, spec)`` – create the Plotly figure

This page contains practical examples for common use cases with wave_view.

Basic Waveform Plot
------------------

Plot input and output voltages from an amplifier simulation:

.. code-block:: python

   import wave_view as wv

   # Load simulation data
   data, metadata = wv.load_spice_raw("amplifier.raw")

   # Simple voltage plot using YAML configuration
   spec = wv.PlotSpec.from_yaml("""
   title: "Amplifier Response"
   x:
    signal: "time"
    label: "Time (s)"
   y:
     - label: "Voltage (V)"
       signals:
         Input: "v(in)"
         Output: "v(out)"
   """)

   fig = wv.plot(data, spec)
   fig.show()

Multi-Y-Axis Plot
----------------

Create multiple strips with shared x-axis and rangeslider:

.. code-block:: python

   data, metadata = wv.load_spice_raw("complete_analysis.raw")

   spec = wv.PlotSpec.from_yaml("""
   title: "Complete Circuit Analysis"
   x:
    signal: "time"
    label: "Time (s)"
   y:
     - label: "Voltage (V)"
       signals:
         Input: "v(in)"
         Output: "v(out)"
     - label: "Current (A)"
       signals:
         M1: "i(m1)"
         M2: "i(m2)"
     - label: "Supply Voltage (V)"
       signals:
         VDD: "v(vdd)"
         VSS: "v(vss)"
    show_rangeslider: true
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
   data_ac, metadata = wv.load_spice_raw("ac_analysis.raw")
   
   # AC signals are automatically returned as complex numbers
   frequency = data_ac["frequency"]  # Real (even though stored as complex)
   v_out = data_ac["v(out)"]         # Complex
   v_in = data_ac["v(in)"]    # complex128 array
   
   print(f"v_out dtype: {v_out.dtype}")  # complex128
   print(f"Is complex: {np.iscomplexobj(v_out)}")  # True

   tf = v_out/v_in
   data_ac["tf_db"] = 20*np.log10(np.abs(tf))
   data_ac["tf_phase"] = np.angle(tf)/np.pi*180

   spec = wv.PlotSpec.from_yaml("""
   title: "Transfer Function Bode Plot"
   x:
    signal: "frequency"
    label: "Frequency (Hz)"
    scale: "log"
   y:
     - label: "Magnitude (dB)"
       signals:
         H(jω): "tf_db"
     - label: "Phase (degrees)"
       signals:
         φ(jω): "tf_phase"
   height: 800
   show_rangeslider: true
   """)

   fig = wv.plot(data_ac, spec)

Comparison Plots
----------------

Compare results from different simulation runs:

.. code-block:: python

   # Load multiple simulations
   data1, _ = wv.load_spice_raw("before_optimization.raw")
   data2, _ = wv.load_spice_raw("after_optimization.raw")

   # Create comparison signals
   data = {
       "v_out_before": data1["v(out)"],
       "v_out_after": data2["v(out)"]
   }

   spec = wv.PlotSpec.from_yaml("""
   title: "Optimization Comparison"
   x:
    signal: "time"
    label: "Time (s)"
   y:
     - label: "Voltage (V)"
       signals:
         Before: "v_out_before"
         After: "v_out_after"
   """)

   fig = wv.plot(data, spec) 