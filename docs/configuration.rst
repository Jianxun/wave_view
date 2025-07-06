Configuration Guide
===================

*wave_view* 1.0.0 uses a single configuration model — :class:`wave_view.PlotSpec` — to describe everything you want to see in a plot.  A PlotSpec is simply structured data (YAML, JSON, or a Python dictionary) that defines:

* **x** – which signal provides the x-axis (usually ``time`` or ``frequency``)
* **y** – one or more groups of y-axis traces
* optional figure-level options such as **title**

This page explains every option, shows practical examples, and demonstrates how to build PlotSpecs from files, strings, or dictionaries.

Creating a PlotSpec
-------------------

.. code-block:: python

   import wave_view as wv

   # from a YAML file
   spec = wv.PlotSpec.from_yaml("config.yaml")

   # from an inline YAML string
   spec = wv.PlotSpec.from_yaml("""
   title: "Transient Analysis"
   x: "time"
   y:
     - label: "Voltage (V)"
       signals: {OUT: "v(out)"}
   """)

   # from a Python dict (raises ValidationError on mistakes)
   dict_spec = {
       "title": "Dict Example",
       "x": "time",
       "y": [{"label": "Current", "signals": {"M1": "i(m1)"}}],
   }
   spec = wv.PlotSpec.model_validate(dict_spec)

Once you have a PlotSpec, pass it to :func:`wave_view.plot` together with either a file path **or** data returned by :func:`wave_view.load_spice_raw`.

YAML / Dict Schema
------------------

Top-level keys
~~~~~~~~~~~~~~

``title`` *(optional)* – Overall figure title.  
``x`` *(required)* – Name of the signal used for the x-axis.  
``y`` *(required)* – A list of **y-axis groups** (each group shares axis formatting).

Y-axis group keys
~~~~~~~~~~~~~~~~~

``label`` *(optional)* – Text shown next to the axis.  
``scale`` *(optional)* – ``linear`` *(default)* or ``log``.  
``signals`` *(required)* – Mapping of legend names to **signal references**.

Signal reference syntax
~~~~~~~~~~~~~~~~~~~~~~~

1. **SPICE trace** – e.g. ``v(out)``, ``i(m1)``  
2. **Processed data** – prefix the key with ``data.`` *or* pass the NumPy array directly and reference it by name.

Example PlotSpec
----------------

.. code-block:: yaml

   title: "Amplifier Analysis"
   x: "time"
   y:
     - label: "Input / Output Voltage (V)"
       signals:
         VIN:  "v(in)"
         VOUT: "v(out)"
     - label: "Current (A)"
       scale: "log"
       signals:
         IM1: "i(m1)"

Processed / Derived Signals
---------------------------

``plot()`` accepts an optional ``processed_data`` dictionary that can be mixed with raw traces.  Reference these arrays with either ``data.<name>`` **or** by the plain legend key if you prefer brevity.

.. code-block:: python

   import numpy as np, wave_view as wv

   data, _ = wv.load_spice_raw("simulation.raw")
   power = data["v(out)"] * data["i(out)"]

   spec = wv.PlotSpec.from_yaml("""
   x: "time"
   y:
     - label: "Voltage & Power"
       signals:
         OUT:   "v(out)"
         Power: "power"   # shorthand for data key
   """)

   fig = wv.plot(data, spec, processed_data={"power": power})

Multiple Configurations
-----------------------

For complex analyses you can create multiple PlotSpecs and call :func:`wave_view.plot` multiple times:

.. code-block:: python

   voltage_spec = wv.PlotSpec.from_yaml("voltage.yaml")
   current_spec = wv.PlotSpec.from_yaml("current.yaml")

   fig_v = wv.plot("simulation.raw", voltage_spec)
   fig_i = wv.plot("simulation.raw", current_spec)

Best Practices
--------------

1. **Use descriptive labels** and include units.  
2. **Group related signals** on the same axis for easy comparison.  
3. Choose **log scales** for signals spanning many orders of magnitude.  
4. Keep YAML files next to your simulations so they can be version-controlled.

---

That's all you need to describe plots with *wave_view* 1.0.0.  Explore the :doc:`quickstart` for an end-to-end example, or dive into :doc:`api` for full symbol documentation. 