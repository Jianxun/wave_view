API Reference
=============

This section documents the public API of the wave_view package. The API follows a clean 3-step workflow:

1. **Discovery**: Use :func:`~wave_view.explore_signals` to discover available signals
2. **Configuration**: Create configuration using :func:`~wave_view.config_from_file` or :func:`~wave_view.config_from_yaml`
3. **Plotting**: Generate plots with :func:`~wave_view.plot`

Main API Functions
------------------

.. currentmodule:: wave_view

.. autosummary::
   :toctree: _autosummary

   plot
   explore_signals
   load_spice
   validate_config
   config_from_file
   config_from_yaml

Core Functions
--------------

.. autofunction:: plot

.. autofunction:: explore_signals

.. autofunction:: load_spice

Configuration Functions
-----------------------

.. autofunction:: validate_config

.. autofunction:: config_from_file

.. autofunction:: config_from_yaml

Core Classes
------------

.. autoclass:: wave_view.SpiceData
   :members:
   :show-inheritance:

.. autoclass:: wave_view.PlotConfig
   :members:
   :show-inheritance:

.. autoclass:: wave_view.SpicePlotter
   :members:
   :show-inheritance: 