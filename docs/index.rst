.. wave_view documentation master file, created by
   sphinx-quickstart on Tue Jun 10 12:19:18 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

wave_view: SPICE Simulation Visualization
=========================================

**wave_view** is a Python package for visualizing SPICE simulation waveforms with a modern, user-friendly API. It provides a clean 3-step workflow for discovering, configuring, and plotting simulation data in Jupyter notebooks.

Features
--------

* **Modern API Design**: Clean 3-step workflow (Discovery → Configuration → Plotting)
* **YAML Configuration**: Flexible configuration system with file, string, or dict input
* **Multi-figure Support**: Create multiple plots from a single configuration
* **Advanced Plotting**: Log scale support, processed data integration, customizable themes
* **Case-insensitive**: All signal names normalized for easy access
* **Path Object Support**: Modern pathlib integration throughout
* **Comprehensive Validation**: Clear error messages guide users to solutions

Quick Start
-----------

.. code-block:: python

   import wave_view as wv

   # Step 1: Discovery - "What's available?"
   signals = wv.explore_signals("simulation.raw")
   print(f"Available signals: {signals}")

   # Step 2: Configuration - "What do I want?"
   config = wv.config_from_yaml("""
   title: "My Simulation Results"
   X:
     signal_key: "time"
     label: "Time (s)"
   Y:
     - label: "Voltage (V)"
       signals:
         OUT: "v(out)"
         IN: "v(in)"
   """)

   # Step 3: Plotting - "Show me the results"
   fig = wv.plot("simulation.raw", config)
   fig.show()

Installation
------------

.. code-block:: bash

   pip install wave_view

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
   examples

.. toctree::
   :maxdepth: 2
   :caption: API Reference:

   api
   core

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

