# Wave View v1.0.0 User Flows and Use Cases

## Overview
This document captures all user flows and use cases for the v1.0.0 architecture. These examples will be used to build comprehensive test cases for the new unified API.

## Current User Flow (v0.2.0) - Multiple Patterns

### Pattern 1: Legacy API
```python
# Current - Legacy approach
spice_file = "./raw_data/tb_ota_5t/test_tran/results.raw"

# Load data
data = wv.load_spice(spice_file)

# Create config
config = wv.config_from_yaml("""
title: "SPICE Simulation"
X:
  signal_key: "raw.time"
  label: "Time (s)"
Y:
  - label: "Voltages (V)"
    signals:
      Input: "v(in)"
      Output: "v(out)"
""")

# Plot (takes file path + config)
fig = wv.plot(spice_file, config, show=True)
```

### Pattern 2: New v0.2.0 API
```python
# Current - New v0.2.0 approach
spice_file = "./raw_data/tb_ota_5t/test_tran/results.raw"

# Load data
data = wv.WaveDataset.from_raw(spice_file, metadata={"temp": 25})

# Create spec
spec = PlotSpec.from_yaml("""
title: "OTA Transient Analysis"
x: "time"
y:
  - label: "Input/Output Voltages (V)"
    signals:
      Input: "v(in)"
      Output: "v(out)"
""")

# Plot (method call)
fig = spec.plot(data)
fig.show()
```

### Pattern 3: With Processed Data
```python
# Current - Processed data approach
spice_file = "./raw_data/tb_ota_5t/test_ac/results.raw"

# Load data
data = wv.load_spice(spice_file)

# Create processed signals
processed_data = {
    "tf_db": 20*np.log10(np.abs(data.get_signal("v(out)"))),
    "tf_phase": np.angle(data.get_signal("v(out)"))
}

# Plot with processed data
fig = wv.plot(spice_file, config=config, processed_data=processed_data, show=True)
```

## New User Flow (v1.0.0) - Unified Pattern

### 🎯 Use Case 1: Basic Single Plot
**Test Case ID**: `test_basic_single_plot`
```python
import wave_view as wv
import numpy as np

# 1. Load data into standard format
data = wv.load_spice("./raw_data/tb_ota_5t/test_tran/results.raw")
# Returns: Dict[str, np.ndarray] = {"time": array([...]), "v(out)": array([...]), ...}

# 2. Create specification (configuration-only)
spec = wv.PlotSpec.from_yaml("""
title: "OTA Transient Analysis"
x: "time"
y:
  - label: "Input/Output Voltages (V)"
    signals:
      Input: "v(in)"
      Output: "v(out)"
""")

# 3. Plot (function-based)
fig = wv.plot(data, spec)
fig.show()
```

### 🔄 Use Case 2: Multiple Plots with Same Data
**Test Case ID**: `test_multiple_plots_same_data`
```python
# Load once, plot multiple times
data = wv.load_spice("simulation.raw")

# Different views of the same data
voltage_spec = wv.PlotSpec.from_yaml("""
title: "Voltage Analysis"
x: "time"
y:
  - label: "Voltages (V)"
    signals:
      Input: "v(in)"
      Output: "v(out)"
""")

current_spec = wv.PlotSpec.from_yaml("""  
title: "Current Analysis"
x: "time"
y:
  - label: "Current (A)"
    signals:
      Supply: "i(vdd)"
""")

# Create multiple figures efficiently
voltage_fig = wv.plot(data, voltage_spec)
current_fig = wv.plot(data, current_spec)

voltage_fig.show()
current_fig.show()
```

### 🧮 Use Case 3: With Data Processing
**Test Case ID**: `test_processed_data_plotting`
```python
# Load raw data
raw_data = wv.load_spice("./raw_data/tb_ota_5t/test_ac/results.raw")

# Process signals (user's responsibility)
processed_data = {
    **raw_data,  # Include all raw signals
    "tf_db": 20*np.log10(np.abs(raw_data["v(out)"])),
    "tf_phase": np.angle(raw_data["v(out)"])
}

# Plot processed data
spec = wv.PlotSpec.from_yaml("""
title: "AC Analysis - Frequency Response"
x: "frequency"
y:
  - label: "Magnitude (dB)"
    signals:
      Magnitude: "tf_db"
  - label: "Phase (deg)"
    signals:
      Phase: "tf_phase"
""")

fig = wv.plot(processed_data, spec)
fig.show()
```

### 📊 Use Case 4: Convenience Functions
**Test Case ID**: `test_convenience_functions`
```python
# One-liner for quick plots
wv.show(data, spec)  # Equivalent to wv.plot(data, spec).show()

# From file directly
spec = wv.PlotSpec.from_file("config.yaml")
fig = wv.plot(data, spec)
```

### 📋 Use Case 5: Configuration from File
**Test Case ID**: `test_config_from_file`
```python
# YAML configuration file: "transient_analysis.yaml"
"""
title: "OTA Transient Analysis"
x: "time"
y:
  - label: "Input/Output Voltages (V)"
    signals:
      Input: "v(in)"
      Output: "v(out)"
  - label: "Supply Current (A)"
    signals:
      I_Supply: "i(v_vdda)"
width: 900
height: 600
show_legend: true
"""

# Load data and config
data = wv.load_spice("simulation.raw")
spec = wv.PlotSpec.from_file("transient_analysis.yaml")

# Plot
fig = wv.plot(data, spec)
fig.show()
```

## User Flow Comparison

### 🔍 Use Case 6: Signal Discovery
**Test Case ID**: `test_signal_discovery`
```python
# Both versions: Start with exploration
signals = wv.explore_signals("simulation.raw")
print(f"Available signals: {signals}")

# Use discovered signals in configuration
spec = wv.PlotSpec.from_yaml(f"""
title: "Discovered Signals"
x: "time"
y:
  - label: "Voltages (V)"
    signals:
      Signal1: "{signals[0]}"
      Signal2: "{signals[1]}"
""")
```

### 📈 Use Case 7: Multi-Axis Plotting
**Test Case ID**: `test_multi_axis_plotting`
```python
data = wv.load_spice("simulation.raw")

spec = wv.PlotSpec.from_yaml("""
title: "Multi-Axis Analysis"
x: "time"
y:
  - label: "Voltages (V)"
    signals:
      Input: "v(in)"
      Output: "v(out)"
      VDD: "v(vdd)"
      
  - label: "Current (mA)"
    signals:
      Supply: "i(vdd)"
      Load: "i(rload)"
      
  - label: "Power (mW)"
    signals:
      Total: "power_total"
""")

fig = wv.plot(data, spec)
fig.show()
```

### 🎨 Use Case 8: Styling and Customization
**Test Case ID**: `test_styling_customization`
```python
data = wv.load_spice("simulation.raw")

spec = wv.PlotSpec.from_yaml("""
title: "Customized Plot"
x: "time"
y:
  - label: "Voltages (V)"
    signals:
      Input: "v(in)"
      Output: "v(out)"

# Styling options
width: 1200
height: 800
theme: "plotly_dark"
title_x: 0.5
title_xanchor: "center"
show_legend: true
grid: true
show_rangeslider: true
""")

fig = wv.plot(data, spec)
fig.show()
```

## Advanced Use Cases

### 🧪 Use Case 9: Complex Signal Processing
**Test Case ID**: `test_complex_signal_processing`
```python
# Load AC analysis data
raw_data = wv.load_spice("ac_analysis.raw")

# Advanced signal processing
processed_data = {
    **raw_data,
    "magnitude_db": 20*np.log10(np.abs(raw_data["v(out)"])),
    "phase_deg": np.angle(raw_data["v(out)"]) * 180/np.pi,
    "group_delay": -np.diff(np.unwrap(np.angle(raw_data["v(out)"]))) / np.diff(raw_data["frequency"]),
    "stability_margin": 180 + np.angle(raw_data["v(out)"]) * 180/np.pi
}

# Plot processed results
spec = wv.PlotSpec.from_yaml("""
title: "AC Analysis - Complete"
x: "frequency"
y:
  - label: "Magnitude (dB)"
    signals:
      Transfer Function: "magnitude_db"
  - label: "Phase (degrees)"
    signals:
      Phase: "phase_deg"
  - label: "Group Delay (ns)"
    signals:
      Group Delay: "group_delay"
""")

fig = wv.plot(processed_data, spec)
fig.show()
```

### 📊 Use Case 10: Batch Processing
**Test Case ID**: `test_batch_processing`
```python
# Process multiple files
files = ["corner_tt.raw", "corner_ss.raw", "corner_ff.raw"]
specs = ["voltage_spec.yaml", "current_spec.yaml", "power_spec.yaml"]

results = []
for file_path in files:
    data = wv.load_spice(file_path)
    
    for spec_path in specs:
        spec = wv.PlotSpec.from_file(spec_path)
        fig = wv.plot(data, spec)
        results.append((file_path, spec_path, fig))
```

### 🔄 Use Case 11: Data Reuse and Efficiency
**Test Case ID**: `test_data_reuse_efficiency`
```python
# Load large dataset once
large_data = wv.load_spice("large_simulation.raw")

# Create multiple analyses without reloading
analyses = {
    "transient": wv.PlotSpec.from_yaml("""
        title: "Transient Analysis"
        x: "time"
        y:
          - label: "Voltages (V)"
            signals:
              Output: "v(out)"
    """),
    
    "frequency": wv.PlotSpec.from_yaml("""
        title: "Frequency Analysis"
        x: "frequency"
        y:
          - label: "Magnitude (dB)"
            signals:
              TF: "tf_magnitude"
    """),
    
    "power": wv.PlotSpec.from_yaml("""
        title: "Power Analysis"
        x: "time"
        y:
          - label: "Power (mW)"
            signals:
              Total: "power_total"
    """)
}

# Generate all plots efficiently
figures = {}
for name, spec in analyses.items():
    figures[name] = wv.plot(large_data, spec)
```

## Migration Use Cases

### 🔄 Use Case 12: Migration from v0.2.0
**Test Case ID**: `test_migration_from_v0_2_0`
```python
# OLD v0.2.0 pattern
def old_approach():
    data = wv.WaveDataset.from_raw("file.raw", metadata={"temp": 25})
    spec = PlotSpec.from_yaml(config_yaml)
    fig = spec.plot(data)
    return fig

# NEW v1.0.0 pattern
def new_approach():
    data = wv.load_spice("file.raw")  # Returns Dict[str, np.ndarray]
    spec = wv.PlotSpec.from_yaml(config_yaml)
    fig = wv.plot(data, spec)
    return fig
```

### ⚠️ Use Case 13: Backward Compatibility (Transition Period)
**Test Case ID**: `test_backward_compatibility`
```python
# Deprecated methods should work with warnings
spec = wv.PlotSpec.from_yaml(config)
data = wv.load_spice("file.raw")

# This should work but emit deprecation warning
with warnings.catch_warnings(record=True) as w:
    fig = spec.plot(data)  # Deprecated method
    assert len(w) == 1
    assert issubclass(w[0].category, DeprecationWarning)
    assert "deprecated" in str(w[0].message)
```

## Future Extensibility Use Cases

### 🚀 Use Case 14: Multi-Case Plotting (Future)
**Test Case ID**: `test_multi_case_plotting_future`
```python
# Future multi-case plotting
pvt_data = wv.load_pvt_corners(["tt.raw", "ss.raw", "ff.raw"])
spec = wv.PlotSpec.from_yaml("""
title: "PVT Corner Analysis"
x: "time"
y:
  - label: "Output Voltage (V)"
    signals:
      Output: "v(out)"
""")

fig = wv.plot_multi_case(pvt_data, spec)
fig.show()
```

### 📈 Use Case 15: Monte Carlo Analysis (Future)
**Test Case ID**: `test_monte_carlo_analysis_future`
```python
# Future Monte Carlo plotting
mc_data = wv.load_monte_carlo("mc_results/")
spec = wv.PlotSpec.from_yaml("""
title: "Monte Carlo Analysis"
x: "time"
y:
  - label: "Output Voltage (V)"
    signals:
      Output: "v(out)"
""")

fig = wv.plot_monte_carlo(mc_data, spec, 
                         confidence_bands=[68, 95],
                         show_mean=True,
                         show_envelope=True)
fig.show()
```

### 🎯 Use Case 16: Parameter Sweep (Future)
**Test Case ID**: `test_parameter_sweep_future`
```python
# Future parameter sweep plotting
sweep_data = wv.load_parameter_sweep("sweep_results/", 
                                    parameter="temperature", 
                                    values=[-40, 27, 85])
spec = wv.PlotSpec.from_yaml("""
title: "Temperature Sweep"
x: "time"
y:
  - label: "Output Voltage (V)"
    signals:
      Output: "v(out)"
""")

fig = wv.plot_parameter_sweep(sweep_data, spec,
                             color_by="temperature",
                             legend_template="{temperature}°C")
fig.show()
```

## Error Handling Use Cases

### ❌ Use Case 17: Missing Signal Error
**Test Case ID**: `test_missing_signal_error`
```python
data = wv.load_spice("file.raw")

# Config references non-existent signal
spec = wv.PlotSpec.from_yaml("""
title: "Test Plot"
x: "time"
y:
  - label: "Voltages (V)"
    signals:
      NonExistent: "v(missing_signal)"
""")

# Should raise clear error
try:
    fig = wv.plot(data, spec)
except ValueError as e:
    assert "missing_signal" in str(e)
    assert "Available signals:" in str(e)
```

### ❌ Use Case 18: Invalid Configuration Error
**Test Case ID**: `test_invalid_config_error`
```python
# Invalid YAML configuration
try:
    spec = wv.PlotSpec.from_yaml("""
    title: "Test Plot"
    x: "time"
    y: "invalid_y_format"  # Should be a list
    """)
except ValueError as e:
    assert "validation error" in str(e).lower()
```

### ❌ Use Case 19: Empty Data Error
**Test Case ID**: `test_empty_data_error`
```python
# Empty data dictionary
empty_data = {}
spec = wv.PlotSpec.from_yaml("""
title: "Test Plot"
x: "time"
y:
  - label: "Voltages (V)"
    signals:
      Output: "v(out)"
""")

try:
    fig = wv.plot(empty_data, spec)
except ValueError as e:
    assert "empty" in str(e).lower() or "no signals" in str(e).lower()
```

## Performance Use Cases

### ⚡ Use Case 20: Large Dataset Handling
**Test Case ID**: `test_large_dataset_performance`
```python
# Large dataset (e.g., 1M+ points)
large_data = wv.load_spice("large_simulation.raw")

# Should handle efficiently
spec = wv.PlotSpec.from_yaml("""
title: "Large Dataset"
x: "time"
y:
  - label: "Voltages (V)"
    signals:
      Output: "v(out)"
""")

import time
start = time.time()
fig = wv.plot(large_data, spec)
end = time.time()

# Should complete within reasonable time
assert end - start < 5.0  # Less than 5 seconds
```

## Summary

These use cases cover:

1. **Basic Functionality**: Single plots, multiple plots, data processing
2. **Configuration**: YAML strings, file loading, styling
3. **Advanced Features**: Multi-axis, complex processing, batch operations
4. **Migration**: From current v0.2.0 to new v1.0.0 pattern
5. **Future Extensibility**: Multi-case, Monte Carlo, parameter sweeps
6. **Error Handling**: Missing signals, invalid configs, empty data
7. **Performance**: Large datasets, efficiency testing

Each use case includes:
- **Test Case ID**: For systematic test implementation
- **Code Example**: Complete working example
- **Context**: When and why this pattern is used
- **Expected Behavior**: What should happen

These will form the foundation for comprehensive test coverage of the v1.0.0 architecture. 