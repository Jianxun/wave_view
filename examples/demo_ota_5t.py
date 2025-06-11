# %%
import wave_view as wv
import numpy as np

# %%

spice_file = "./raw_data/tb_ota_5t/test_tran/results.raw"

data = wv.load_spice(spice_file)

print(f"Total signals: {len(data.signals)}")
for signal in data.signals:
    print(f"  - {signal}")


# Now proceed with plotting using YAML configuration
custom_config = wv.config_from_yaml("""
title: "SPICE Simulation - Key Signals"

X:
  signal_key: "raw.time"
  label: "Time (s)"

Y:
  - label: "Voltages (V)"
    signals:
      Input: "v(in)"
      Output: "v(out)"
      VDDA: "v(vdda)"
      VSSA: "v(vssa)"
      
  - label: "Current (A)"
    signals:
      Supply Current: "i(v_vdda)"

plot_height: 600
show_zoom_buttons: true
show_rangeslider: true
""")

fig1 = wv.plot(spice_file, custom_config, show=True)

# %%
# CORRECTED: AC Analysis with Processed Data using plot() function
print("🔧 AC Analysis with Processed Data - CORRECTED")

spice_file = "./raw_data/tb_ota_5t/test_ac/results.raw"
data = wv.load_spice(spice_file)

print(f"Total signals: {len(data.signals)}")
for signal in data.signals:
    print(f"  - {signal}")

# Compute processed signals (dB conversion: 20*log10 for voltage)
processed_data = {
    "vdb_out": 20 * np.log10(np.abs(data.get_signal("v(out)"))),
    "vdb_in": 20 * np.log10(np.abs(data.get_signal("v(in)")))
}

# YAML config referencing processed signals with "data." prefix
# Using log scale for frequency axis (typical for Bode plots)
ac_config = wv.config_from_yaml("""
title: "AC Analysis - Frequency Response (Bode Plot)"

X:
  signal_key: "raw.frequency"
  label: "Frequency (Hz)"
  scale: log

Y:
  - label: "Magnitude (dB)"
    signals:
      Input: "data.vdb_in"
      Output: "data.vdb_out"

plot_height: 600
show_zoom_buttons: False
show_rangeslider: true
""")

# Create figure using the new processed_data parameter
fig2 = wv.plot(spice_file, ac_config, processed_data=processed_data, show=True)

print("✅ AC analysis with processed data created successfully!")

# %%

spice_file = "./raw_data/tb_ota_5t/test_ac/results.raw"

data = wv.load_spice(spice_file)

#print(f"Total signals: {len(data.signals)}")
#for signal in data.signals:
#    print(f"  - {signal}")

processed_data = {
    "tf_db" : 20*np.log10(np.abs(data.get_signal("v(out)"))),
    "tf" : np.abs(data.get_signal("v(out)"))
}

print(processed_data)



# Now proceed with plotting using YAML configuration
custom_config = wv.config_from_yaml("""
title: "SPICE Simulation - Key Signals"

X:
  signal_key: "frequency"
  label: "Frequency (Hz)"
  scale: "log"

Y:
  - label: "Voltages (V)"
    signals:
      Output: "data.tf_db"
    

plot_height: 600
show_rangeslider: true
""")

fig2 = wv.plot(spice_file, config=custom_config, processed_data=processed_data, show=True)

# %%
