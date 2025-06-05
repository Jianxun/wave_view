# %%
"""
Jupyter Notebook Demo - Wave View Package
==========================================

Run this in a Jupyter notebook to test inline plotting.
Each cell can be run independently.
"""

import sys
sys.path.insert(0, './wave_view')
import wave_view as wv

# %%
# 0. Manual renderer control (optional)
print("🎛️ Manual renderer control...")

# Force inline display (useful if auto-detection fails)
wv.set_renderer("notebook")  

# Other options:
# wv.set_renderer("browser")     # Force browser
# wv.set_renderer("auto")        # Auto-detect (default)

# %%
# 1. Load and explore SPICE data
print("🔍 Loading SPICE data...")
data = wv.load_spice("prototype/script/Ring_Oscillator_7stage.raw")
print(f"📊 Found {len(data.signals)} signals")
print(f"⚡ Sample signals: {data.signals[:8]}")

# %%
# 2. Quick auto-plot (should appear inline in notebook)
print("🚀 Creating automatic plot...")
fig1 = wv.plot("prototype/script/Ring_Oscillator_7stage.raw")
print("✅ Plot should appear above (inline in notebook)")

# %%
# 3. Custom configuration plot
print("⚙️ Creating custom plot...")

custom_config = {
    "title": "Ring Oscillator - Custom View",
    "X": {"signal_key": "raw.time", "label": "Time (s)"},
    "Y": [
        {
            "label": "Key Voltages (V)",
            "signals": {
                "VDD": "v(vdd)", 
                "Output": "v(bus06)",
                "Node 7": "v(bus07)"
            }
        }
    ],
    "plot_height": 500
}

fig2 = wv.plot("prototype/script/Ring_Oscillator_7stage.raw", custom_config)
print("✅ Custom plot should appear above")

# %%
# 4. Advanced plotter with signal processing
print("🧮 Advanced plotting with signal processing...")

plotter = wv.SpicePlotter("prototype/script/Ring_Oscillator_7stage.raw")

# Add processed signals
plotter.add_processed_signal("power", lambda d: d["v(vdd)"] * d["i(c1)"])
plotter.add_processed_signal("output_inverted", lambda d: -d["v(bus06)"])

# Create plot with processed signals
processed_config = {
    "title": "Processed Signals",
    "X": {"signal_key": "raw.time", "label": "Time (s)"},
    "Y": [
        {
            "label": "Processed Data",
            "signals": {
                "Power (W)": "data.power",
                "Inverted Output": "data.output_inverted"
            }
        }
    ]
}

plotter.load_config(processed_config)
plotter.show()  # Should appear inline

print("✅ Processed signals plot should appear above")

# %%
# 5. Environment detection test
from wave_view.api import _is_jupyter_environment

print(f"🔍 Jupyter environment detected: {_is_jupyter_environment()}")
print(f"📊 Current Plotly renderer: {wv.pio.renderers.default}")

if _is_jupyter_environment():
    print("✅ Running in Jupyter - plots should appear inline")
else:
    print("🌐 Running standalone - plots will open in browser")

# %% 