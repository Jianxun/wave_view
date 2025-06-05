
# %%
import sys
import os

# Add the package to path (in real usage, this would be: pip install wave_view)
sys.path.insert(0, './wave_view')

import wave_view as wv


# Use the test data we have available
spice_file = "prototype/script/Ring_Oscillator_7stage.raw"

data = wv.load_spice(spice_file)

custom_config = {
    "title": "Ring Oscillator - Key Nodes",
    "X": {
        "signal_key": "raw.time", 
        "label": "Time (s)"
    },
    "Y": [
        {
            "label": "Voltages (V)",
            "signals": {
                "VDD": "v(vdd)",
                "Output": "v(bus06)",
                "Bus07": "v(bus07)"
            }
        },
        {
            "label": "Current (A)", 
            "signals": {
                "Supply Current": "i(c1)"
            }
        }
    ],
    "plot_height": 600,
    "show_rangeslider": True
}

fig1 = wv.plot(spice_file, custom_config, show=True)
# %%
