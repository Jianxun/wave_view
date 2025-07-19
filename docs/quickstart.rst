Quick Start Guide
=================

This guide provides two common workflows for using ``waveview`` to visualize your SPICE simulations.

* **Option A: CLI-First** – The fastest way to get from a ``.raw`` file to an interactive plot. Perfect for quick, one-off visualizations.
* **Option B: Python API** – The most flexible approach. Ideal for scripting, custom data processing, and embedding plots in notebooks or reports.

Choose the workflow that best fits your needs.

Option A: CLI-First Workflow
----------------------------

Get from a raw file to a plot in three steps using the ``waveview`` command-line tool.

**Step 1: Generate a Plot Specification**

Use ``waveview init`` to create a template ``spec.yaml`` file from your simulation output. It automatically populates the file with the independent variable (like "time") and a few available signals.

.. code-block:: bash

   waveview init your_simulation.raw > spec.yaml

**Step 2: Discover Signals**

Find the exact names of the signals you want to plot with ``waveview signals``.

.. code-block:: bash

   # List the first 10 signals
   waveview signals your_simulation.raw

   # List all signals
   waveview signals your_simulation.raw --all

   # Filter signals using a regular expression
   waveview signals your_simulation.raw --grep "v(out)"

**Step 3: Plot**

Edit your ``spec.yaml`` to include the signals you discovered, then use ``waveview plot`` to generate an interactive HTML file or display the plot directly.

.. code-block:: bash

   # This command will open a browser window with your plot
   waveview plot spec.yaml

   # To save the plot to a file instead
   waveview plot spec.yaml --output my_plot.html

This approach is fast, requires no Python code, and keeps your plot configuration version-controlled alongside your simulation files.

Option B: Python API Workflow
-----------------------------

For more advanced use cases, the Python API provides full control over data loading, processing, and plotting. This is ideal for Jupyter notebooks, custom analysis scripts, and automated report generation.

The API follows a clear three-step workflow:

1.  **Data Loading** – Load the raw ``.raw`` file with :func:`wave_view.load_spice_raw`.
2.  **Configuration** – Describe what you want to see using :class:`wave_view.PlotSpec`.
3.  **Plotting** – Call :func:`wave_view.plot` to get a Plotly figure.

**Minimal Example**

.. code-block:: python

   import wave_view as wv

   # 1. Load data from a .raw file
   data, _ = wv.load_spice_raw("your_simulation.raw")
   print(f"Signals available: {list(data.keys())[:5]}...")

   # 2. Configure the plot using a YAML string
   spec = wv.PlotSpec.from_yaml("""
   title: "My Simulation Results"
   x:
     signal: "time"
     label: "Time (s)"
   y:
     - label: "Voltage (V)"
       signals:
         Output: "v(out)"
         Input:  "v(in)"
   """)

   # 3. Create and display the plot
   fig = wv.plot(data, spec)
   fig.show()

**Advanced Example: Plotting Derived Signals**

Because the API gives you direct access to the data as NumPy arrays, you can easily perform calculations and plot the results.

.. code-block:: python

   import numpy as np
   import wave_view as wv

   # Load the data
   data, _ = wv.load_spice_raw("your_simulation.raw")

   # Calculate a new, derived signal
   data["diff_voltage"] = data["v(out_p)"] - data["v(out_n)"]

   # Create a spec that plots both raw and derived signals
   spec = wv.PlotSpec.from_yaml("""
   title: "Differential Output Voltage"
   x:
     signal: "time"
     label: "Time (s)"
   y:
     - label: "Voltage (V)"
       signals:
         VOUT_P: "v(out_p)"
         VOUT_N: "v(out_n)"
         VOUT_DIFF: "diff_voltage"
   """)

   # Create and display the plot
   fig = wv.plot(data, spec)
   fig.show()

Next Steps
----------

*   Dive into the :doc:`configuration` guide for all available YAML options.
*   Browse the :doc:`cli` reference for more command-line features.
*   Consult the :doc:`api` reference for full details on each function. 