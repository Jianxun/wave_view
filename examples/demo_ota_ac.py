import wave_view as wv
import numpy as np

spice_file = "examples/raw_data/tb_ota_5t/test_ac/results.raw"
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
    signal: "frequency"
    label: "Frequency (Hz)"
    log_scale: true
y:
  - label: "Magnitude (dB)"
    signals:
      Input: "vdb_in"
      Output: "vdb_out"

height: 600
show_rangeslider: true
""")

# Create figure using the new processed_data parameter
fig2 = wv.plot(data, ac_spec, show=True)

print("✅ AC analysis with processed data created successfully!")