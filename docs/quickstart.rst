Quick Start Guide
=================

This guide shows how to create interactive SPICE plots with *wave_view* 1.0.0 in just a few lines of code.  The API follows a clear three-step workflow:

1. **Data Loading** – Load the raw ``.raw`` file with :func:`wave_view.load_spice_raw` (returns a plain ``dict`` of NumPy arrays).
2. **Configuration** – Describe what you want to see using :class:`wave_view.PlotSpec`.  You can build a spec from a YAML file, a YAML string, or a Python dictionary.
3. **Plotting** – Call :func:`wave_view.plot` to obtain an interactive Plotly figure that you can show, save, or embed.


The Three-Step Workflow
-----------------------

Step 1  Data Loading *(optional)*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you want immediate access to the data – e.g. for inspection or custom post-processing – load the file first:

.. code-block:: python

   import wave_view as wv

   data, metadata = wv.load_spice_raw("simulation.raw")
   print(f"Found {len(data)} signals → {list(data)[:5]} …")

``load_spice_raw`` returns a dictionary mapping signal names to NumPy arrays and a small metadata dictionary.  *All* plotting examples in v1.0.0 assume a pre-loaded ``data`` dictionary.

Step 2  Configuration with PlotSpec
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a plot description with :class:`~wave_view.PlotSpec`.  Two common patterns are shown below.

**(a) YAML file**

.. code-block:: yaml
   :caption: config.yaml

   title: "My SPICE Results"
   x: 
    signal: "time"
    label: "Time (s)"
   y:
     - label: "Voltage (V)"
       signals:
         OUT: "v(out)"
         IN:  "v(in)"

.. code-block:: python

   spec = wv.PlotSpec.from_file("config.yaml")

**(b) Inline YAML string**

.. code-block:: python

   spec = wv.PlotSpec.from_yaml("""
   title: "Quick Demo"
   x: 
    signal: "time"
    label: "Time (s)"
   y:
     - label: "Output Voltage"
       signals:
         OUT: "v(out)"
   """)

**(c) Pure Python dictionary**

.. code-block:: python

   dict_config = {
       "title": "Dict Config Example",
       "x": {"signal": "time", "label": "Time (s)"},
       "y": [
           {"label": "Voltage", "signals": {"OUT": "v(out)"}}
       ],
   }
   spec = wv.PlotSpec.model_validate(dict_config)  # validation happens here

Step 3  Plotting
~~~~~~~~~~~~~~~~

Generate your figure with a single call:

.. code-block:: python

   # Plot using the pre-loaded dictionary
   fig = wv.plot(data, spec)

   # Display inside Jupyter
   fig.show()

   # Or export
   fig.write_html("my_plot.html")
   fig.write_image("my_plot.png")

Minimal Example
------------------------

.. code-block:: python

   import wave_view as wv

   # Optional data inspection
   data, _ = wv.load_spice_raw("simulation.raw")
   print(list(data)[:10])

   # Build configuration
   spec = wv.PlotSpec.from_yaml("""
   x: 
    signal: "time"
    label: "Time (s)"
   y:
     - label: "Voltage (V)"
       signals: 
         OUT: "v(out)"
   """)

   # Plot
   fig = wv.plot(data, spec)
   fig.show()

Advanced Topics
---------------

Processed / Derived Signals
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Because ``load_spice_raw`` returns ordinary NumPy arrays, you can derive new signals and plot them alongside raw traces:

.. code-block:: python

   import numpy as np
   import wave_view as wv

   data, _ = wv.load_spice_raw("simulation.raw")
   v_diff = data["v(node2)"] - data["v(node1)"]  # custom calculation

   # Add derived signal to the dictionary
   data["v_diff"] = v_diff

   spec = wv.PlotSpec.from_yaml("""
   x: 
    signal: "time"
    label: "Time (s)"
   y:
     - label: "Voltage"
       signals:
         OUT:   "v(out)"
         V_diff: "v_diff"
   """)

   fig = wv.plot(data, spec)

Next Steps
----------

* Dive into the :doc:`configuration` guide for every available option.  
* Browse :doc:`examples` for real-world use cases.  
* Consult the :doc:`api` reference for full symbol documentation. 