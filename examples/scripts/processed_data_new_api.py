# %%
"""
Processed Data API Demo for Wave View

This script demonstrates the new processed_data parameter in the plot() function.
The processed_data parameter accepts a dictionary of {signal_name: numpy_array}
which can then be referenced in YAML config using "data.signal_name".
"""

import wave_view as wv
import numpy as np

# %%
print("=== Wave View Processed Data API ===\n")

# %%
# Example 1: Basic AC Analysis with dB conversion
print("📊 Example 1: AC Analysis with dB Conversion")
print("=" * 50)

spice_file = "../data/tb_ota_5t/test_ac/results.raw"
data = wv.load_spice(spice_file)

print(f"Available signals: {data.signals}")

# Compute processed signals
processed_data = {
    "vdb_out": 20 * np.log10(np.abs(data.get_signal("v(out)"))),
    "vdb_in": 20 * np.log10(np.abs(data.get_signal("v(in)"))),
    "phase_out": np.angle(data.get_signal("v(out)")) * 180 / np.pi
}

print(f"Created processed signals: {list(processed_data.keys())}")

# YAML config using processed signals
ac_config = """
title: "AC Analysis - Frequency Response"

X:
  signal_key: "raw.frequency"
  label: "Frequency (Hz)"

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

# Plot using the new API
fig1 = wv.plot(spice_file, ac_config, processed_data=processed_data, show=False)
print("✅ AC analysis plot created")

# %%
# Example 2: Transient Analysis with Power Calculation
print("\n⚡ Example 2: Transient Analysis with Power")
print("=" * 50)

spice_file_tran = "../data/tb_ota_5t/test_tran/results.raw"
data_tran = wv.load_spice(spice_file_tran)

print(f"Available signals: {data_tran.signals}")

# Compute power and other processed signals
processed_data_tran = {
    # Power calculation (assuming we have voltage and current signals)
    "power_supply": data_tran.get_signal("v(vdda)") * data_tran.get_signal("i(v_vdda)"),
    
    # Differential signal (if we have complementary signals)
    "v_diff": data_tran.get_signal("v(out)") - data_tran.get_signal("v(in)"),
    
    # Simple moving average (basic filtering)
    "v_out_avg": np.convolve(data_tran.get_signal("v(out)"), np.ones(10)/10, mode='same')
}

print(f"Created processed signals: {list(processed_data_tran.keys())}")

# YAML config for transient analysis
tran_config = """
title: "Transient Analysis with Processed Signals"

X:
  signal_key: "raw.time"
  label: "Time (s)"

Y:
  - label: "Raw Voltages (V)"
    signals:
      Input: "v(in)"
      Output: "v(out)"
      Supply: "v(vdda)"
      
  - label: "Processed Signals"
    signals:
      Differential: "data.v_diff"
      Output (Averaged): "data.v_out_avg"
      
  - label: "Power (W)"
    signals:
      Supply Power: "data.power_supply"

plot_height: 800
show_rangeslider: true
"""

# Plot using processed data
fig2 = wv.plot(spice_file_tran, tran_config, processed_data=processed_data_tran, show=False)
print("✅ Transient analysis with processed signals created")

# %%
# Example 3: Complex Processing with Multiple Functions
print("\n🔬 Example 3: Advanced Signal Processing")
print("=" * 50)

# More advanced signal processing
def moving_rms(signal, window=50):
    """Calculate moving RMS of a signal."""
    return np.sqrt(np.convolve(signal**2, np.ones(window)/window, mode='same'))

def derivative(signal, time_step=1e-9):
    """Calculate numerical derivative."""
    return np.gradient(signal, time_step)

# Apply advanced processing
time_data = data_tran.get_signal("time")
out_signal = data_tran.get_signal("v(out)")

advanced_processed = {
    "v_out_rms": moving_rms(out_signal),
    "v_out_derivative": derivative(out_signal, np.mean(np.diff(time_data))),
    "power_envelope": np.abs(data_tran.get_signal("v(vdda)") * data_tran.get_signal("i(v_vdda)"))
}

print(f"Created advanced processed signals: {list(advanced_processed.keys())}")

advanced_config = """
title: "Advanced Signal Processing Example"

X:
  signal_key: "raw.time"
  label: "Time (s)"

Y:
  - label: "Original Signal (V)"
    signals:
      Output: "v(out)"
      
  - label: "RMS & Derivative"
    signals:
      RMS: "data.v_out_rms"
      dV/dt: "data.v_out_derivative"
      
  - label: "Power Envelope (W)"
    signals:
      Power Envelope: "data.power_envelope"

plot_height: 900
show_rangeslider: true
"""

# Create advanced plot
fig3 = wv.plot(spice_file_tran, advanced_config, processed_data=advanced_processed, show=False)
print("✅ Advanced signal processing plot created")

# %%
# Summary
print(f"\n🎯 Summary: New Processed Data API")
print("=" * 50)
print("✅ Three examples created successfully:")
print("   1. AC Analysis with dB conversion and phase")
print("   2. Transient analysis with power and differential signals")
print("   3. Advanced processing with RMS, derivatives, and envelopes")
print("\n💡 Key Features:")
print("   • processed_data parameter accepts {signal_name: numpy_array}")
print("   • Reference in YAML config with 'data.signal_name'")
print("   • No need to expose internal SpicePlotter class")
print("   • Clean, simple API for complex signal processing")

# Show all figures
print("\n🖼️  Displaying all figures...")
fig1.show()
fig2.show()
fig3.show()

# %% 