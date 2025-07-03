# %%
"""
Demo: New PlotSpec API - Wave View v0.2.0

This demo showcases the new PlotSpec Pydantic-based API that provides:
- Structured validation with type safety
- Fluent API for cleaner code
- Better IDE support and error messages
- Efficient data reuse (parse once, plot multiple times)
"""

import wave_view as wv
import numpy as np
from wave_view.core.plotspec import PlotSpec

print("🚀 Wave View v0.2.0 - New PlotSpec API Demo")
print("=" * 50)

# %%
print("\n1️⃣ **NEW API**: PlotSpec.from_yaml() + fluent plotting")
print("-" * 50)

# Load SPICE data once - efficient!
spice_file = "./raw_data/tb_ota_5t/test_tran/results.raw"
data = wv.load_spice(spice_file)

print(f"✅ Loaded SPICE data: {len(data.signals)} signals")

# Create PlotSpec using the new Pydantic model
transient_spec = PlotSpec.from_yaml("""
title: "OTA Transient Analysis - New PlotSpec API"
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

# Fluent API - clean and readable!
fig1 = transient_spec.plot(data)
fig1.show()

print("✅ Created transient plot with new PlotSpec API")

# %%
print("\n2️⃣ **EFFICIENT WORKFLOW**: Parse once, plot multiple times")
print("-" * 50)

# Same data object - no re-parsing!
# Create a second plot with different configuration
dc_characteristics_spec = PlotSpec.from_yaml("""
title: "DC Characteristics - Voltage Analysis"
x: "time" 
y:
  - label: "Differential Signals (V)"
    signals:
      "Input-Output": "v(in)"
      "Output": "v(out)"
    log_scale: false
    
width: 800
height: 400
grid: true
zoom_buttons: true
""")

# Reuse the same data - very efficient!
fig2 = dc_characteristics_spec.plot(data)
fig2.show()

print("✅ Created second plot efficiently (no file re-parsing)")

# %%
print("\n3️⃣ **AC ANALYSIS**: Complex signals with processed data")
print("-" * 50)

# Load AC analysis data
ac_file = "./raw_data/tb_ota_5t/test_ac/results.raw"
ac_data = wv.load_spice(ac_file)

print(f"✅ Loaded AC data: {len(ac_data.signals)} signals")

# Process complex AC signals 
processed_signals = {
    "gain_db": 20 * np.log10(np.abs(ac_data.get_signal("v(out)"))),
    "phase_deg": np.angle(ac_data.get_signal("v(out)")) * 180 / np.pi,
    "input_db": 20 * np.log10(np.abs(ac_data.get_signal("v(in)")))
}

print("✅ Processed complex AC signals (magnitude, phase)")

# Create Bode plot specification
bode_spec = PlotSpec.from_yaml("""
title: "AC Analysis - Bode Plot (PlotSpec API)"
x: "frequency"
y:
  - label: "Magnitude (dB)"
    signals:
      "Gain (Output)": "data.gain_db"
      "Input Level": "data.input_db"
      
  - label: "Phase (degrees)"
    signals:
      "Phase": "data.phase_deg"

width: 1000
height: 600
title_x: 0.5
grid: true
show_legend: true
""")

# Plot with processed data
fig3 = bode_spec.plot(ac_data, processed_data=processed_signals)
fig3.show()

print("✅ Created Bode plot with processed signals")

# %%
print("\n4️⃣ **COMPARISON**: Old API vs New PlotSpec API")
print("-" * 50)

print("🔄 OLD API (v0.1.0):")
print("""
# Multiple file parsings, verbose configuration
config = wv.config_from_yaml(yaml_string)
fig = wv.plot("file.raw", config)  # ← Re-parses file each time
""")

print("\n🚀 NEW API (v0.2.0):")
print("""
# Parse once, efficient reuse, cleaner syntax
data = wv.load_spice("file.raw")     # ← Parse once
spec = PlotSpec.from_yaml(yaml_str)  # ← Pydantic validation
fig = spec.plot(data)                # ← Fluent API, reuse data
""")

# %%
print("\n5️⃣ **PROGRAMMATIC USAGE**: Build PlotSpec in code")
print("-" * 50)

# Create PlotSpec programmatically (not just from YAML)
from wave_view.core.plotspec import YAxisSpec

programmatic_spec = PlotSpec(
    title="Programmatically Created Plot",
    x="time",
    y=[
        YAxisSpec(
            label="Voltages (V)",
            signals={"VDD": "v(vdda)", "OUT": "v(out)"},
            log_scale=False
        ),
        YAxisSpec(
            label="Current (A)", 
            signals={"Supply": "i(v_vdda)"},
            log_scale=True  # Log scale for current
        )
    ],
    width=800,
    height=500,
    title_x=0.5,
    title_xanchor="center",
    show_legend=True,
    grid=True
)

# Plot using programmatically created spec
fig4 = programmatic_spec.plot(data)
fig4.show()

print("✅ Created plot from programmatically built PlotSpec")

# %%
print("\n6️⃣ **VALIDATION DEMO**: Pydantic error handling")
print("-" * 50)

try:
    # This will show nice Pydantic validation errors
    invalid_spec = PlotSpec.from_yaml("""
    title: "Invalid Configuration"
    # Missing required 'x' field
    y:
      - label: "Test"
        # Missing required 'signals' field
    """)
except Exception as e:
    print(f"🚨 Validation Error (expected): {type(e).__name__}")
    print(f"   Message: {str(e)}")

print("✅ Pydantic provides rich validation with helpful error messages")

# %%
print("\n" + "=" * 50)
print("🎉 **PlotSpec API Demo Complete!**")
print("\n**Key Benefits Demonstrated:**")
print("✅ Type-safe configuration with Pydantic validation")
print("✅ Fluent API: spec.plot(data) for clean code")
print("✅ Efficient workflow: parse once, plot multiple times")
print("✅ YAML + Programmatic configuration support")
print("✅ Multi-axis and processed signal support")
print("✅ Rich error messages for invalid configurations")
print("\n🚀 Ready for Wave View v0.2.0!") 