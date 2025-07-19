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
   spec = wv.PlotSpec.from_file("config.yaml")

   # from an inline YAML string
   spec = wv.PlotSpec.from_yaml("""
   title: "Transient Analysis"
   x: 
    signal: "time"
    label: "Time (s)"
   y:
     - label: "Voltage (V)"
       signals: {OUT: "v(out)"}
   """)

   # from a Python dict (raises ValidationError on mistakes)
   dict_spec = {
       "title": "Dict Example",
       "x": {"signal": "time", "label": "Time (s)"},
       "y": [{"label": "Current", "signals": {"M1": "i(m1)"}}],
   }
   spec = wv.PlotSpec.model_validate(dict_spec)

Once you have a PlotSpec, pass it to :func:`wave_view.plot` together with the *data* dictionary returned by :func:`wave_view.load_spice_raw`.

Schema Reference
----------------

For the complete field-by-field documentation of all configuration options, see the :doc:`schema` reference page, which is automatically generated from the Pydantic model definitions.

Example PlotSpec
----------------

Here's a comprehensive example showing common configuration options:

.. code-block:: yaml

   title: "Amplifier Analysis"
   x: 
    signal: "time"
    label: "Time (s)"
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

To plot *derived* signals just insert them into the same ``data`` dictionary – they behave exactly like native SPICE traces.

.. code-block:: python

   import numpy as np, wave_view as wv

   data, _ = wv.load_spice_raw("simulation.raw")
   power = data["v(out)"] * data["i(out)"]

   # Append the derived signal to the data dict
   data["power"] = power

   spec = wv.PlotSpec.from_yaml("""
   x: 
    signal: "time"
    label: "Time (s)"
   y:
     - label: "Voltage & Power"
       signals:
         OUT:   "v(out)"
         Power: "power"   # shorthand for data key
   """)

   fig = wv.plot(data, spec)

Multiple Configurations
-----------------------

For complex analyses you can create multiple PlotSpecs and call :func:`wave_view.plot` multiple times:

.. code-block:: python

   voltage_spec = wv.PlotSpec.from_file("voltage.yaml")
   current_spec = wv.PlotSpec.from_file("current.yaml")

   data, _ = wv.load_spice_raw("simulation.raw")
   fig_v = wv.plot(data, voltage_spec)
   fig_i = wv.plot(data, current_spec)

Best Practices
--------------

1. **Use descriptive labels** and include units.  
2. **Group related signals** on the same axis for easy comparison.  
3. Choose **log scales** for signals spanning many orders of magnitude.  
4. Keep YAML files next to your simulations so they can be version-controlled.

---

That's all you need to describe plots with *wave_view* 1.0.0.  Explore the :doc:`quickstart` for an end-to-end example, or dive into :doc:`api` for full symbol documentation. 