
"""
Demo: New v0.2.0 API - PlotSpec + WaveDataset

This demo showcases the new v0.2.0 API architecture that provides:
- WaveDataset: Modern data container with metadata support  
- PlotSpec: Structured validation with type safety
- Fluent API for cleaner code
- Better IDE support and error messages
- Efficient data reuse (parse once, plot multiple times)
"""

import wave_view as wv
import numpy as np
from wave_view.core.plotspec import PlotSpec
import plotly.io as pio

# Configure Plotly for standalone execution (not notebook)
pio.renderers.default = 'browser'

print("🚀 Wave View v0.2.0 - New API Demo")
print("=" * 50)


print("\n1️⃣ **NEW v0.2.0 API**: WaveDataset + PlotSpec")
print("-" * 50)

# New API: WaveDataset with metadata support
spice_file = "./raw_data/tb_ota_5t/test_tran/results.raw"
metadata = {
    "simulation": "transient_analysis",
    "circuit": "ota_5t", 
    "temperature": 25,
    "corner": "typical"
}

# Load SPICE data with metadata - the modern way!
data = wv.WaveDataset.from_raw(spice_file, metadata=metadata)

print(f"✅ Loaded SPICE data: {len(data.signals)} signals")
print(f"📊 Metadata: {data.metadata}")
print(f"🔧 Available signals: {data.signals[:5]}...")

# Create PlotSpec using the new Pydantic model
transient_spec = PlotSpec.from_yaml("""
title: "OTA Transient Analysis - New v0.2.0 API"
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

width: 900
height: 600
title_x: 0.5
show_legend: true
""")

# New v0.2.0 API pattern: WaveDataset → PlotSpec → Figure
fig1 = transient_spec.plot(data)
fig1.show()

print("✅ Created transient plot with new v0.2.0 API")