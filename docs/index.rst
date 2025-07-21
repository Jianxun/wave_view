.. yaml2plot documentation master file, created by
   sphinx-quickstart on Tue Jun 10 12:19:18 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

yaml2plot: A Python Toolkit for SPICE Simulation Waveform Visualization
========================================================================

*yaml2plot* is a modern Python toolkit for turning raw SPICE ``.raw`` files into beautiful, interactive Plotly graphs.  Version 2.0.0 introduces a simple **three-step workflow**:

1. **Data Loading** – load with :func:`yaml2plot.load_spice_raw`.  
2. **Configuration** – describe your plot in YAML, JSON, or a Python dict using :class:`yaml2plot.PlotSpec`.  
3. **Plotting** – call :func:`yaml2plot.plot` and get an interactive figure you can display, embed, or export.

Features
--------

* **Clean API** – only four public symbols: ``load_spice_raw``, ``PlotSpec``, ``plot``, and ``WaveDataset``.  
* **YAML-first configuration** – version-controlled plot specs that live next to your simulations.  
* **Processed-data integration** – mix NumPy-derived signals with raw traces in a single call.  
* **Automatic renderer detection** – works seamlessly in Jupyter, VS Code, or standalone scripts.

Quick Start
-----------

.. code-block:: python

   import yaml2plot as y2p

   # Optional: inspect the data first
   data, _ = y2p.load_spice_raw("simulation.raw")
   print(f"Signals → {list(data)[:5]} …")

   # Build a plot description (YAML, dict, or inline YAML as below)
   spec = y2p.PlotSpec.from_yaml("""
   title: "My Simulation Results"
   x: 
    signal: "time"
    label: "Time (s)"
   y:
     - label: "Voltage (V)"
       signals:
         OUT: "v(out)"
         IN:  "v(in)"
   """)

   # Create the plot (pass the file path *or* pre-loaded data)
   fig = y2p.plot(data, spec)
   fig.show()

Installation
------------

.. code-block:: bash

   pip install yaml2plot

For development:

.. code-block:: bash

   pip install -e ".[dev]"

Contents
--------

.. toctree::
   :maxdepth: 2
   :caption: User Guide:

   installation
   quickstart
   configuration
   schema
   cli
   examples

.. toctree::
   :maxdepth: 2
   :caption: API Reference:

   api

.. toctree::
   :maxdepth: 1
   :caption: Development:

   changelog
   contributing

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

