# %%
import wave_view as wv
import numpy as np

# %%

# ────────────────────────────────────────────────────────────────────────────
# Time-domain transient example – v1.0.0 API
# ────────────────────────────────────────────────────────────────────────────
spice_file = "./raw_data/tb_ota_5t/test_tran/results.raw"

# v1.0.0 loader returns (data_dict, metadata)
data, _ = wv.load_spice_raw(spice_file)

print(f"Total signals: {len(data)}")
for signal in data:
    print(f"  - {signal}")

custom_spec = wv.PlotSpec.from_yaml("""
title: "SPICE Simulation - Key Signals"

x: "time"

y:
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

fig1 = wv.plot(data, custom_spec, show=True)

# %%
# CORRECTED: AC Analysis with Processed Data using plot() function
print("🔧 AC Analysis with Processed Data - CORRECTED")

# ────────────────────────────────────────────────────────────────────────────
# AC analysis – add derived dB traces directly into *data*
# ────────────────────────────────────────────────────────────────────────────
spice_file = "./raw_data/tb_ota_5t/test_ac/results.raw"
data, _ = wv.load_spice_raw(spice_file)

print(f"Total signals: {len(data)}")
for signal in data:
    print(f"  - {signal}")

# Append processed (dB) signals to the data dict
data["vdb_out"] = 20 * np.log10(np.abs(data["v(out)"]))
data["vdb_in"] = 20 * np.log10(np.abs(data["v(in)"]))

ac_spec = wv.PlotSpec.from_yaml("""
title: "AC Analysis - Frequency Response (Bode Plot)"

x:
  signal_key: "frequency"
  label: "Frequency (Hz)"
  scale: log

y:
  - label: "Magnitude (dB)"
    signals:
      Input: "vdb_in"
      Output: "vdb_out"

plot_height: 600
show_rangeslider: true
""")

# Create figure using the new processed_data parameter
fig2 = wv.plot(data, ac_spec, show=True)

print("✅ AC analysis with processed data created successfully!")

# %%

# ────────────────────────────────────────────────────────────────────────────
# Single-trace magnitude example (tf_db)
# ────────────────────────────────────────────────────────────────────────────
spice_file = "./raw_data/tb_ota_5t/test_ac/results.raw"

data, _ = wv.load_spice_raw(spice_file)

data["tf_db"] = 20 * np.log10(np.abs(data["v(out)"]))
data["tf"] = np.abs(data["v(out)"])

print({"tf_db": data["tf_db"], "tf": data["tf"]})

custom_spec = wv.PlotSpec.from_yaml("""
title: "SPICE Simulation - Key Signals"

X: "frequency"
  
Y:
  - label: "Voltages (V)"
    signals:
      Output: "tf_db"
    

plot_height: 600
show_rangeslider: true
""")

fig2 = wv.plot(data, custom_spec)

# %%
# ────────────────────────────────────────────────────────────────────────────
# Magnitude & phase example
# ────────────────────────────────────────────────────────────────────────────
spice_file = "./raw_data/tb_ota_5t/test_ac/results.raw"

data, _ = wv.load_spice_raw(spice_file)

data["tf_db"] = 20 * np.log10(np.abs(data["v(out)"]))
data["tf_phase"] = np.angle(data["v(out)"]) * 180 / np.pi

print({"tf_db": data["tf_db"], "tf_phase": data["tf_phase"]})

custom_spec = wv.PlotSpec.from_yaml("""
title: "AC Analysis - Frequency Response"

X:
  signal_key: "frequency"
  label: "Frequency (Hz)"
  scale: "log"
                                    
Y:
  - label: "Magnitude (dB)"
    signals:
      Magnitude: "data.tf_db"
  - label: "Phase (deg)"
    signals:
      Phase: "data.tf_phase"

                                    
plot_height: 600
show_zoom_buttons: false
show_rangeslider: true
""")

fig2 = wv.plot(data, custom_spec, show=True)

# %%
