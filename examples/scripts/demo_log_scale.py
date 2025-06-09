# %%
"""
Log Scale Demo for Wave View

This script demonstrates the new log scale functionality for both X and Y axes.
Perfect for frequency response plots (Bode plots) and other logarithmic data.
"""

import wave_view as wv
import numpy as np

# %%
print("=== Wave View Log Scale Demo ===\n")

# %%
# Example 1: AC Analysis with Log Frequency Axis (Typical Bode Plot)
print("📊 Example 1: AC Analysis with Log Frequency Axis")
print("=" * 50)

spice_file = "../data/tb_ota_5t/test_ac/results.raw"
data = wv.load_spice(spice_file)

print(f"Available signals: {data.signals}")

# Compute processed signals for magnitude in dB
processed_data = {
    "vdb_out": 20 * np.log10(np.abs(data.get_signal("v(out)"))),
    "vdb_in": 20 * np.log10(np.abs(data.get_signal("v(in)"))),
    "phase_out": np.angle(data.get_signal("v(out)")) * 180 / np.pi
}

print(f"Created processed signals: {list(processed_data.keys())}")

# Bode plot configuration with log frequency axis
bode_config = """
title: "Bode Plot - AC Analysis with Log Frequency Scale"

X:
  signal_key: "raw.frequency"
  label: "Frequency (Hz)"
  scale: log

Y:
  - label: "Magnitude (dB)"
    signals:
      Input: "data.vdb_in"
      Output: "data.vdb_out"
      
  - label: "Phase (degrees)"
    signals:
      Output Phase: "data.phase_out"

plot_height: 700
show_rangeslider: true
"""

# Plot Bode plot with log frequency axis
fig1 = wv.plot(spice_file, bode_config, processed_data=processed_data, show=False)
print("✅ Bode plot with log frequency axis created")

# %%
# Example 2: Linear vs Log Scale Comparison
print("\n📈 Example 2: Linear vs Log Scale Comparison")
print("=" * 50)

# Same data, linear frequency axis
linear_config = """
title: "Linear Frequency Scale - AC Analysis"

X:
  signal_key: "raw.frequency"
  label: "Frequency (Hz)"
  scale: linear

Y:
  - label: "Magnitude (dB)"
    signals:
      Output: "data.vdb_out"

plot_height: 500
show_rangeslider: true
"""

fig2 = wv.plot(spice_file, linear_config, processed_data=processed_data, show=False)
print("✅ Linear frequency scale plot created")

# %%
# Example 3: Log Scale on Y-Axis (Power/Magnitude)
print("\n⚡ Example 3: Log Scale on Y-Axis")
print("=" * 50)

# For power calculations, sometimes log scale is useful
spice_file_tran = "../data/tb_ota_5t/test_tran/results.raw"
data_tran = wv.load_spice(spice_file_tran)

# Calculate absolute power and other signals
processed_power = {
    "power_abs": np.abs(data_tran.get_signal("v(vdda)") * data_tran.get_signal("i(v_vdda)")),
    "v_out_abs": np.abs(data_tran.get_signal("v(out)")),
    "current_abs": np.abs(data_tran.get_signal("i(v_vdda)"))
}

# Configuration with log Y-axis for power
power_log_config = """
title: "Power Analysis with Log Y-Scale"

X:
  signal_key: "raw.time"
  label: "Time (s)"

Y:
  - label: "Voltage (V) - Linear"
    signals:
      Output: "v(out)"
      
  - label: "Absolute Power (W) - Log Scale"
    scale: log
    signals:
      Supply Power: "data.power_abs"
      
  - label: "Current (A) - Log Scale"
    scale: log
    signals:
      Supply Current: "data.current_abs"

plot_height: 900
show_rangeslider: true
"""

fig3 = wv.plot(spice_file_tran, power_log_config, processed_data=processed_power, show=False)
print("✅ Power analysis with log Y-scale created")

# %%
# Example 4: Both X and Y Log Scales
print("\n🔬 Example 4: Both X and Y Log Scales")
print("=" * 50)

# Create magnitude response with both axes in log scale
magnitude_config = """
title: "Magnitude Response - Both Axes Log Scale"

X:
  signal_key: "raw.frequency"
  label: "Frequency (Hz)"
  scale: log

Y:
  - label: "Magnitude (Linear Scale) - Log Y Axis"
    scale: log
    signals:
      Input Magnitude: "data.abs_v_in"
      Output Magnitude: "data.abs_v_out"

plot_height: 600
show_rangeslider: true
"""

# Compute linear magnitude (not dB)
magnitude_data = {
    "abs_v_in": np.abs(data.get_signal("v(in)")),
    "abs_v_out": np.abs(data.get_signal("v(out)"))
}

fig4 = wv.plot(spice_file, magnitude_config, processed_data=magnitude_data, show=False)
print("✅ Both axes log scale plot created")

# %%
# Summary and Display
print(f"\n🎯 Summary: Log Scale Features")
print("=" * 50)
print("✅ Four examples created successfully:")
print("   1. Bode plot with log frequency axis (typical use case)")
print("   2. Comparison: linear vs log frequency scale")
print("   3. Log Y-axis for power analysis")
print("   4. Both X and Y axes in log scale")
print("\n💡 Log Scale Configuration:")
print("   • Add 'scale: log' to X or Y axis configuration")
print("   • X-axis: under 'X' section")
print("   • Y-axis: under individual Y axis in 'Y' list")
print("   • Default scale is 'linear' (no need to specify)")
print("\n🔧 YAML Examples:")
print("   X-axis log: X: {signal_key: 'frequency', scale: log}")
print("   Y-axis log: Y: [{label: 'Power', scale: log, signals: {...}}]")

# Show all figures
print("\n🖼️  Displaying all figures...")
fig1.show()
fig2.show()
fig3.show()
fig4.show()

# %% 