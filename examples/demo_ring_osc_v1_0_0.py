import wave_view as wv

# v1.0.0 API Demo: Function-based plotting with Dict[str, np.ndarray] data
# Architecture: load_spice_raw() → Dict[str, np.ndarray] → PlotSpec → plot() → Figure
# Note: Plotly renderer is now configured automatically on import!

# New v1.0.0 API: Load SPICE data directly in Dict format
spice_file = "./raw_data/tb_ota_5t/test_tran/results.raw"

# Load SPICE data directly in v1.0.0 format: Dict[str, np.ndarray]
data, metadata = wv.load_spice_raw(spice_file)

print(f"Loaded SPICE data: {len(data)} signals")
print(f"Available signals: {list(data.keys())[:10]}...")
print(f"Metadata: {metadata}")

# Create PlotSpec using the new v1.0.0 configuration-only model
ps_tran = wv.PlotSpec.from_yaml("""
title: "OTA Transient Analysis - New v1.0.0 API"
x: "time"
y:
  - label: "Input/Output Voltages (V)"
    signals:
      Input: "v(in)"
      Output: "v(out)"
      
  - label: "Supply Voltages (V)"
    signals:
      VDDA: "v(vdda)"
      VSSA: "v(vssa)"
      
  - label: "Supply Current (A)"
    signals:
      I_Supply: "i(v_vdda)"

#width: 900
height: 800
show_legend: true
show_rangeslider: true
""")

# New v1.0.0 API pattern: Dict[str, np.ndarray] → PlotSpec → Figure
fig1 = wv.plot(spice_file, ps_tran)
# fig1.show() is called automatically by plot() with show=True (default)
