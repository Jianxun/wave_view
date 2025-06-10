Configuration Guide
===================

wave_view uses a flexible configuration system based on YAML/dictionary structures. This guide covers all available configuration options and how to use them effectively.

Configuration Formats
----------------------

You can provide configuration in three ways:

Python Dictionary
~~~~~~~~~~~~~~~~~

.. code-block:: python

   config = {
       "title": "My Plots",
       "plots": [...]
   }
   fig = wv.plot("simulation.raw", config)

YAML File
~~~~~~~~~

.. code-block:: yaml

   # config.yaml
   title: "My Plots"
   plots:
     - ...

.. code-block:: python

   config = wv.config_from_file("config.yaml")
   fig = wv.plot("simulation.raw", config)

YAML String
~~~~~~~~~~~

.. code-block:: python

   yaml_config = """
   title: "My Plots"
   plots:
     - ...
   """
   config = wv.config_from_yaml(yaml_config)
   fig = wv.plot("simulation.raw", config)

Root Configuration Options
--------------------------

title
~~~~~

Optional overall title for the entire figure.

.. code-block:: yaml

   title: "SPICE Simulation Results"

plots
~~~~~

Required list of plot configurations. Each plot becomes a subplot in the final figure.

.. code-block:: yaml

   plots:
     - signals: ["v(out)"]
       title: "Output Voltage"
     - signals: ["i(m1)"]
       title: "Current"

Plot Configuration Options
--------------------------

Each plot in the `plots` list can have the following options:

Required Options
~~~~~~~~~~~~~~~~

signals
*******

List of signal names to plot. Signal names are case-insensitive.

.. code-block:: yaml

   signals: ["v(out)", "v(in)", "I(R1)"]

Optional Options
~~~~~~~~~~~~~~~~

title
*****

Title for this specific plot.

.. code-block:: yaml

   title: "Voltage Waveforms"

xlabel
******

X-axis label. Defaults to "Time".

.. code-block:: yaml

   xlabel: "Time (s)"

ylabel
******

Y-axis label. If not specified, attempts to auto-generate from signal types.

.. code-block:: yaml

   ylabel: "Voltage (V)"

log_x
*****

Enable logarithmic scale for X-axis. Default: false.

.. code-block:: yaml

   log_x: true

log_y
*****

Enable logarithmic scale for Y-axis. Default: false.

.. code-block:: yaml

   log_y: true

grid
****

Show grid lines. Default: true.

.. code-block:: yaml

   grid: false

legend
******

Show legend. Default: true.

.. code-block:: yaml

   legend: false

Complete Example
----------------

Here's a comprehensive configuration example showing all available options:

.. code-block:: yaml

   title: "Amplifier Analysis"
   plots:
     - signals: ["v(in)", "v(out)"]
       title: "Input vs Output Voltage"
       xlabel: "Time (s)"
       ylabel: "Voltage (V)"
       grid: true
       legend: true
       
     - signals: ["i(m1)", "i(m2)"]
       title: "Transistor Currents"
       ylabel: "Current (A)"
       log_y: true
       
     - signals: ["v(vdd)", "v(vss)"]
       title: "Supply Voltages"
       ylabel: "Supply (V)"
       grid: false

Multi-Figure Support
--------------------

wave_view can create multiple separate figures from a single configuration. This is useful when you want different plot layouts or when plots have very different scales.

Single Figure (Default)
~~~~~~~~~~~~~~~~~~~~~~~

All plots become subplots in one figure:

.. code-block:: python

   config = {
       "plots": [
           {"signals": ["v(out)"]},
           {"signals": ["i(m1)"]}
       ]
   }
   fig = wv.plot("simulation.raw", config)  # Returns single figure

Multiple Figures
~~~~~~~~~~~~~~~~

To create separate figures, make `plots` a list of lists:

.. code-block:: python

   config = {
       "plots": [
           [{"signals": ["v(out)"]}],           # Figure 1
           [{"signals": ["i(m1)", "i(m2)"]}]   # Figure 2
       ]
   }
   figures = wv.plot("simulation.raw", config)  # Returns list of figures

Processed Data Integration
--------------------------

You can include computed signals alongside SPICE data by using the `processed_data` parameter:

.. code-block:: python

   # Compute processed signals
   spice_data = wv.load_spice("simulation.raw")
   processed_signals = {
       "power": spice_data.get_signal_data("v(out)") * spice_data.get_signal_data("i(out)"),
       "efficiency": compute_efficiency(spice_data)
   }

   config = {
       "plots": [
           {
               "signals": ["v(out)", "power"],  # Mix SPICE and processed data
               "title": "Voltage and Power"
           }
       ]
   }

   fig = wv.plot("simulation.raw", config, processed_data=processed_signals)

Signal Name Handling
--------------------

Case Insensitivity
~~~~~~~~~~~~~~~~~~

All signal names are normalized to lowercase for easy access:

.. code-block:: python

   # These are all equivalent:
   signals: ["V(OUT)", "v(out)", "V(Out)", "v(OUT)"]

Automatic Categorization
~~~~~~~~~~~~~~~~~~~~~~~~

Signals are automatically categorized by type:

* **Voltage signals**: Start with "v(" - e.g., "v(out)", "v(vdd)"
* **Current signals**: Start with "i(" - e.g., "i(m1)", "i(r1)"  
* **Other signals**: Everything else - e.g., "time", "frequency"

Configuration Validation
-------------------------

Use :func:`~wave_view.validate_config` to check your configuration:

.. code-block:: python

   config = {
       "plots": [
           {"signals": ["v(out)"]}
       ]
   }

   errors = wv.validate_config(config)
   if errors:
       print("Configuration errors:")
       for error in errors:
           print(f"  - {error}")
   else:
       print("Configuration is valid!")

Common Validation Errors
~~~~~~~~~~~~~~~~~~~~~~~~

* Missing `plots` key
* Empty `plots` list
* Plot missing `signals` key
* Empty `signals` list
* Invalid data types (e.g., string instead of list for signals)

Best Practices
--------------

1. **Use descriptive titles**: Help users understand what each plot shows
2. **Specify units in labels**: Make axes clear with proper units
3. **Group related signals**: Put related signals in the same plot for comparison
4. **Use log scales appropriately**: For signals spanning multiple orders of magnitude
5. **Validate configurations**: Always check configuration validity before plotting
6. **Use YAML files**: For complex configurations, YAML files are more maintainable than dictionaries 