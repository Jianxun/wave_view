import yaml2plot as wv
import numpy as np

spice_file = "./raw_data/tb_ota_5t/test_ac/results.raw"

data, metadata = wv.load_spice_raw(spice_file)

data["tf_db"] = 20*np.log10(np.abs(data["v(out)"]))
data["tf_phase"] = np.angle(data["v(out)"])/np.pi*180

# Now proceed with plotting using YAML configuration
spec = wv.PlotSpec.from_yaml("""
title: "AC Analysis - Frequency Response"

X:
  signal: "frequency"
  label: "Frequency (Hz)"
  scale: "log"
                                    
Y:
  - label: "Magnitude (dB)"
    signals:
      Magnitude: "tf_db"
  - label: "Phase (deg)"
    signals:
      Phase: "tf_phase"        
height: 600
width: 800
show_rangeslider: true
""")

fig2 = wv.plot(data, spec)