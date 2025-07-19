API Reference
=============

wave_view 1.0.0 exposes a streamlined, function-oriented public API built around three explicit steps:

1. **Data Loading** – Load raw SPICE data into Python with :func:`wave_view.load_spice_raw` *or* let :func:`wave_view.plot` load it lazily from a file path.
2. **Configuration** – Describe what you want to plot using :class:`wave_view.PlotSpec` (YAML, file, or dictionary input).
3. **Plotting** – Call :func:`wave_view.plot` to generate an interactive Plotly figure.

This page documents each public symbol in the order you will use them.

Main API Symbols
----------------

.. currentmodule:: wave_view

.. autosummary::
   :toctree: _autosummary

   plot
   load_spice_raw
   PlotSpec
   WaveDataset 