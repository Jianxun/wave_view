# %%
"""
YAML String Demo - Wave View Package
====================================

This demo shows how to use YAML string blocks directly instead of
dictionaries or separate files for configuration.
"""

import sys
sys.path.insert(0, './wave_view')
import wave_view as wv

# %%
# Example 1: Simple YAML string configuration
print("📝 Using YAML string for configuration...")

yaml_config = """
title: "Ring Oscillator - YAML String Config"
X:
  signal_key: "raw.time"
  label: "Time (s)"
Y:
  - label: "Supply Voltages (V)"
    signals:
      VDD: "v(vdd)"
      Output: "v(bus06)"
  - label: "Current (A)"
    signals:
      Supply: "i(c1)"
plot_height: 600
show_rangeslider: true
"""

# Use the YAML string directly
fig1 = wv.plot("prototype/script/Ring_Oscillator_7stage.raw", yaml_config)
print("✅ Plot created with YAML string config")

# %%
# Example 2: Multi-line YAML with advanced features
print("🔧 Advanced YAML string configuration...")

advanced_yaml = """
title: "Advanced Ring Oscillator Analysis"
X:
  signal_key: "raw.time"
  label: "Time (s)"
Y:
  - label: "Digital Signals (V)"
    signals:
      "Node 5": "v(bus05)"
      "Node 6": "v(bus06)" 
      "Node 7": "v(bus07)"
      "Node 8": "v(bus08)"
  - label: "Power Supply (V)"
    signals:
      VDD: "v(vdd)"
      
plot_height: 700
show_rangeslider: true
show_zoom_buttons: true
default_dragmode: "zoom"
"""

fig2 = wv.plot("prototype/script/Ring_Oscillator_7stage.raw", advanced_yaml, show=False)
print("✅ Advanced plot created with YAML string")

# %%
# Example 3: Using YAML strings with SpicePlotter
print("🚀 YAML strings with advanced plotter...")

plotter = wv.SpicePlotter("prototype/script/Ring_Oscillator_7stage.raw")

# Add some processed signals
plotter.add_processed_signal("power", lambda d: d["v(vdd)"] * d["i(c1)"])

# YAML config that uses processed signals
processed_yaml = """
title: "Processed Signal Analysis"
X:
  signal_key: "raw.time"
  label: "Time (s)"
Y:
  - label: "Raw Signals"
    signals:
      "VDD": "v(vdd)"
      "Output": "v(bus06)"
  - label: "Processed Signals"  
    signals:
      "Power": "data.power"
"""

plotter.load_config(processed_yaml)
fig3 = plotter.create_figure()
print("✅ SpicePlotter with YAML string config")

# %%
# Example 4: Validation with YAML strings
print("🔍 Validating YAML string configurations...")

# Test validation
warnings = wv.validate_config(yaml_config, "prototype/script/Ring_Oscillator_7stage.raw")
if warnings:
    print("⚠️  Configuration warnings:")
    for warning in warnings:
        print(f"   • {warning}")
else:
    print("✅ YAML string configuration is valid")

# %%
# Example 5: Template to YAML string workflow
print("📋 Template generation and YAML string usage...")

# Generate a template file
wv.create_config_template("temp_template.yaml", "prototype/script/Ring_Oscillator_7stage.raw")

# Read it as a string
with open("temp_template.yaml", "r") as f:
    template_yaml = f.read()

print("📄 Generated template as YAML string:")
print(template_yaml[:300] + "..." if len(template_yaml) > 300 else template_yaml)

# Use the template string directly
fig4 = wv.plot("prototype/script/Ring_Oscillator_7stage.raw", template_yaml, show=False)
print("✅ Used generated template as YAML string")

# Clean up
import os
os.remove("temp_template.yaml")

# %%
# Example 6: Multi-figure YAML string
print("📊 Multi-figure YAML string...")

multi_figure_yaml = """
- title: "Figure 1 - Supply Voltage"
  X:
    signal_key: "raw.time"
    label: "Time (s)"
  Y:
    - label: "Supply (V)"
      signals:
        VDD: "v(vdd)"

- title: "Figure 2 - Digital Outputs"  
  X:
    signal_key: "raw.time"
    label: "Time (s)"
  Y:
    - label: "Digital Nodes (V)"
      signals:
        "Bus 6": "v(bus06)"
        "Bus 7": "v(bus07)"
"""

# This would create multiple figures (just validate for now)
config = wv.PlotConfig(multi_figure_yaml)
print(f"✅ Multi-figure config: {config.figure_count} figures")

print("\n🎉 YAML string configuration demo complete!")
print("\n💡 Key benefits:")
print("   • No separate files needed")
print("   • Easy to copy/paste in notebooks") 
print("   • Version control friendly")
print("   • Same features as file-based configs")

# %% 