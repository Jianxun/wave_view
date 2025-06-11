Quick Start Guide
=================

This guide will get you up and running with wave_view in just a few minutes. We'll walk through the 3-step workflow that makes wave_view easy to use.

The 3-Step Workflow
-------------------

wave_view follows a simple, explicit workflow:

1. **Discovery**: Explore what signals are available in your SPICE file
2. **Configuration**: Define what you want to plot
3. **Plotting**: Generate the visualization

Step 1: Discovery
-----------------

First, let's see what signals are available in your SPICE simulation file:

.. code-block:: python

   import wave_view as wv

   # Explore available signals
   signals = wv.explore_signals("path/to/your/simulation.raw")
   print(signals)

This returns a dictionary with categorized signals:

.. code-block:: python

   {
       'voltage_signals': ['v(out)', 'v(in)', 'v(vdd)'],
       'current_signals': ['i(m1)', 'i(r1)'],
       'other_signals': ['time']
   }

Step 2: Configuration
---------------------

Next, create a configuration that defines what you want to plot using YAML format:

.. code-block:: yaml

   # config.yaml
   title: "My SPICE Results"
   X:
     signal_key: "time"
     label: "Time (s)"
   Y:
     - label: "Voltage (V)"
       signals:
         OUT: "v(out)"
         IN: "v(in)"
     - label: "Current (A)"
       scale: "log"
       signals:
         M1: "i(m1)"

.. code-block:: python

   config = wv.config_from_file("config.yaml")

Step 3: Plotting
----------------

Finally, generate your plot:

.. code-block:: python

   # Create the plot
   fig = wv.plot("path/to/your/simulation.raw", config)
   
   # Display in Jupyter notebook
   fig.show()
   
   # Or save to file
   fig.write_html("my_plot.html")
   fig.write_image("my_plot.png")

Complete Example
----------------

Here's a complete working example:

.. code-block:: python

   import wave_view as wv

   # Step 1: Discover available signals
   signals = wv.explore_signals("simulation.raw")
   print(f"Found {len(signals['voltage_signals'])} voltage signals")

   # Step 2: Configure what to plot (using YAML)
   config = wv.config_from_yaml("""
   title: "SPICE Simulation Results"
   X:
     signal_key: "time"
     label: "Time (s)"
   Y:
     - label: "Voltage (V)"
       signals:
         OUT: "v(out)"
         IN: "v(in)"
   """)

   # Step 3: Generate the plot
   fig = wv.plot("simulation.raw", config)
   fig.show()

Advanced Features
-----------------

Processed Data
~~~~~~~~~~~~~~

You can include computed signals alongside SPICE data:

.. code-block:: python

   import numpy as np

   # Load SPICE data
   spice_data = wv.load_spice("simulation.raw")
   time = spice_data.get_signal_data("time")
   
   # Compute processed signal
   processed_signals = {
       "power": spice_data.get_signal_data("v(out)") * spice_data.get_signal_data("i(out)")
   }

   config = wv.config_from_yaml("""
   X:
     signal_key: "time"
     label: "Time (s)"
   Y:
     - label: "Voltage and Power"
       signals:
         OUT: "v(out)"
         Power: "data.power"
   """)

   fig = wv.plot("simulation.raw", config, processed_data=processed_signals)

AC Analysis with Complex Numbers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

wave_view automatically handles complex numbers from AC analysis for transfer function analysis:

.. code-block:: python

   import numpy as np

   # Load AC analysis data (contains complex numbers)
   spice_data = wv.load_spice("ac_analysis.raw")
   v_out = spice_data.get_signal("v(out)")  # Complex numbers preserved
   
   # Process for Bode plot
   processed_signals = {
       "magnitude_db": 20 * np.log10(np.abs(v_out)),
       "phase_deg": np.angle(v_out) * 180 / np.pi
   }

   config = wv.config_from_yaml("""
   title: "Bode Plot"
   X:
     signal_key: "frequency"
     label: "Frequency (Hz)"
     scale: "log"
   Y:
     - label: "Magnitude (dB)"
       signals:
         Output: "data.magnitude_db"
     - label: "Phase (°)"
       signals:
         Phase: "data.phase_deg"
   """)

   fig = wv.plot("ac_analysis.raw", config, processed_data=processed_signals)

Configuration Validation
~~~~~~~~~~~~~~~~~~~~~~~~

Validate your configuration before plotting:

.. code-block:: python

   config = wv.config_from_file("config.yaml")  # Your YAML configuration
   
   # Check if configuration is valid
   errors = wv.validate_config(config)
   if errors:
       print("Configuration errors:")
       for error in errors:
           print(f"  - {error}")
   else:
       print("Configuration is valid!")
       fig = wv.plot("simulation.raw", config)

Next Steps
----------

* Learn more about :doc:`configuration` options
* Explore :doc:`examples` for common use cases
* Check the :doc:`api` reference for detailed documentation 