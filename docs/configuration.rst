Configuration Guide
===================

wave_view uses a flexible configuration system based on YAML/dictionary structures. This guide covers all available configuration options and how to use them effectively.

Configuration Formats
----------------------

You can provide configuration in three ways:

YAML Configuration (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

wave_view uses YAML configuration files for defining plots. While dictionaries are still supported, YAML is the recommended approach.

YAML File
~~~~~~~~~

.. code-block:: yaml

   # config.yaml
   title: "My Plots"
   X:
     signal_key: "time"
     label: "Time (s)"
   Y:
     - label: "Voltage"
       signals:
         VDD: "v(vdd)"

.. code-block:: python

   config = wv.config_from_file("config.yaml")
   fig = wv.plot("simulation.raw", config)

YAML String
~~~~~~~~~~~

.. code-block:: python

   yaml_config = """
   title: "My Plots"
   X:
     signal_key: "time"
     label: "Time (s)"
   Y:
     - label: "Voltage"
       signals:
         VDD: "v(vdd)"
   """
   config = wv.config_from_yaml(yaml_config)
   fig = wv.plot("simulation.raw", config)

Configuration Structure
-----------------------

The configuration uses an X/Y axis structure that clearly separates what you want on each axis:

.. code-block:: yaml

   title: "Optional overall title"
   X:
     signal_key: "time"    # Required: X-axis data source
     label: "Time (s)"         # Optional: X-axis label  
     scale: "linear"           # Optional: "linear" or "log"
   Y:
     - label: "Voltage (V)"    # Optional: Y-axis group label
       scale: "linear"         # Optional: "linear" or "log" 
       signals:               # Required: signals to plot
         VDD: "v(vdd)"        # Legend name: signal reference
         OUT: "v(out)"

Root Configuration Options
--------------------------

title
~~~~~

Optional overall title for the entire figure.

.. code-block:: yaml

   title: "SPICE Simulation Results"

X (Required)
~~~~~~~~~~~~

Defines the X-axis configuration. Always required.

.. code-block:: yaml

   X:
     signal_key: "time"    # Signal to use for X-axis
     label: "Time (s)"         # Axis label (optional)
     scale: "linear"           # "linear" or "log" (optional, default: linear)

Y (Required)  
~~~~~~~~~~~~

List of Y-axis groups. Each group can contain multiple signals that share the same Y-axis properties.

.. code-block:: yaml

   Y:
     - label: "Voltage (V)"
       scale: "linear"
       signals:
         VDD: "v(vdd)"
         OUT: "v(out)"
     - label: "Current (A)" 
       scale: "log"
       signals:
         M1: "i(m1)"

Y-Axis Group Options
~~~~~~~~~~~~~~~~~~~~

label
*****

Optional label for this Y-axis group.

.. code-block:: yaml

   label: "Voltage (V)"

scale
*****

Scale type for this Y-axis group. Can be "linear" or "log". Default: "linear".

.. code-block:: yaml

   scale: "log"

signals (Required)
******************

Dictionary mapping legend names to signal references. Each signal reference can be:

- ``signal_name`` - Signal from SPICE file (default)
- ``data.signal_name`` - Processed signal (passed via processed_data parameter)

.. code-block:: yaml

   signals:
     VDD: "v(vdd)"            # SPICE signal reference
     OUT: "v(out)"            # SPICE signal reference  
     Power: "data.power"      # Processed signal reference

Complete Example
----------------

Here's a comprehensive configuration example showing all available options:

.. code-block:: yaml

   title: "Amplifier Analysis"
   X:
     signal_key: "time"
     label: "Time (s)"
     scale: "linear"
   Y:
     - label: "Input/Output Voltage (V)"
       scale: "linear"
       signals:
         Input: "v(in)"
         Output: "v(out)"
     - label: "Transistor Currents (A)"
       scale: "log"
       signals:
         M1: "i(m1)"
         M2: "i(m2)"
     - label: "Supply Voltages (V)"
       scale: "linear"
       signals:
         VDD: "v(vdd)"
         VSS: "v(vss)"

Alternative Approaches
--------------------

If you need different plot layouts, simply create separate configurations and call :func:`~wave_view.plot` multiple times:

.. code-block:: python

   # Create separate configurations for different analyses
   voltage_config = wv.config_from_yaml("""
   title: "Voltage Analysis"
   X:
     signal_key: "time"
     label: "Time (s)"
   Y:
     - label: "Voltage (V)"
       signals:
         OUT: "v(out)"
         IN: "v(in)"
   """)

   current_config = wv.config_from_yaml("""
   title: "Current Analysis"  
   X:
     signal_key: "time"
     label: "Time (s)"
   Y:
     - label: "Current (A)"
       signals:
         M1: "i(m1)"
         M2: "i(m2)"
   """)

   # Create separate figures
   voltage_fig = wv.plot("simulation.raw", voltage_config)
   current_fig = wv.plot("simulation.raw", current_config)

This approach provides more flexibility and cleaner separation of concerns.

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

   config = wv.config_from_yaml("""
   title: "Voltage and Power Analysis"
   X:
     signal_key: "time"
     label: "Time (s)"
   Y:
     - label: "Mixed Signals"
       signals:
         Voltage: "v(out)"      # SPICE signal
         Power: "data.power"    # Processed signal
   """)

   fig = wv.plot("simulation.raw", config, processed_data=processed_signals)

Signal Name Handling
--------------------

Case Insensitivity
~~~~~~~~~~~~~~~~~~

All signal names are normalized to lowercase for easy access:

.. code-block:: python

   # These are all equivalent in signal references:
   OUT: "V(OUT)"    # Same as v(out)
   OUT: "v(out)"    # Same as V(OUT)
   OUT: "V(Out)"    # Same as v(out)

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

   config = wv.config_from_yaml("""
   X:
     signal_key: "time"
   Y:
     - signals:
         OUT: "v(out)"
   """)

   errors = wv.validate_config(config)
   if errors:
       print("Configuration errors:")
       for error in errors:
           print(f"  - {error}")
   else:
       print("Configuration is valid!")

Common Validation Errors
~~~~~~~~~~~~~~~~~~~~~~~~

* Missing `X` or `Y` configuration
* Missing `signal_key` in X configuration
* Y configuration not a list
* Y-axis group missing `signals` key
* Invalid signal references
* Invalid data types (e.g., string instead of dict for signals)

Best Practices
--------------

1. **Use descriptive titles**: Help users understand what each plot shows
2. **Specify units in labels**: Make axes clear with proper units
3. **Group related signals**: Put related signals in the same plot for comparison
4. **Use log scales appropriately**: For signals spanning multiple orders of magnitude
5. **Validate configurations**: Always check configuration validity before plotting
6. **Use YAML files**: For complex configurations, YAML files are more maintainable than dictionaries 