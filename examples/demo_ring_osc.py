# %%
import wave_view as wv

# Use the test data we have available
spice_file = "./raw_data/Ring_Oscillator_7stage.raw"

data = wv.load_spice(spice_file)

custom_config = wv.config_from_yaml("""
title: "Ring Oscillator - Key Nodes"

X:
  signal_key: "raw.time"
  label: "Time (s)"

Y:
  - label: "Voltages (V)"
    signals:
      VDD: "v(vdd)"
      Output: "v(bus06)"
      Bus07: "v(bus07)"
      
  - label: "Current (A)"
    signals:
      Supply Current: "i(c1)"

plot_height: 600
show_rangeslider: true
""")

fig1 = wv.plot(spice_file, custom_config, show=True)
# %%

# Demonstrate creating separate figures with different configurations
spice_file = "./raw_data/Ring_Oscillator_7stage.raw"

data = wv.load_spice(spice_file)

# First figure configuration
config1 = wv.config_from_yaml("""
title: "Ring Oscillator - All Key Nodes"

X:
  signal_key: "raw.time"
  label: "Time (s)"

Y:
  - label: "Voltages (V)"
    signals:
      VDD: "v(vdd)"
      Output: "v(bus06)"
      Bus07: "v(bus07)"
      
  - label: "Current (A)"
    signals:
      Supply Current: "i(c1)"

plot_height: 600
show_rangeslider: true
""")

# Second figure configuration (focused on output signals)
config2 = wv.config_from_yaml("""
title: "Ring Oscillator - Output Analysis"

X:
  signal_key: "raw.time"
  label: "Time (s)"

Y:
  - label: "Output Voltages (V)"
    signals:
      Output: "v(bus06)"
      Bus07: "v(bus07)"

plot_height: 600
show_rangeslider: true
""")

# Create separate figures 
fig2 = wv.plot(spice_file, config1, show=True)
fig3 = wv.plot(spice_file, config2, show=True)
# %%
