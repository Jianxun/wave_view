# Wave View Implementation Plan

## Package Structure

```
wave_view/
├── __init__.py                 # Main API exports
├── core/
│   ├── __init__.py
│   ├── reader.py              # SPICE raw file reading
│   ├── plotter.py             # Plotly plotting engine
│   ├── config.py              # YAML config handling
│   └── processor.py           # Signal processing utilities
├── utils/
│   ├── __init__.py
│   ├── validators.py          # Input validation
│   └── templates.py           # YAML templates and examples
├── examples/
│   ├── __init__.py
│   ├── configs/               # Example YAML configs
│   └── notebooks/             # Example Jupyter notebooks
└── tests/
    └── ...
```

## Proposed API Design

### Simple API (90% of use cases)
```python
import wave_view as wv

# Simplest usage - auto-display in Jupyter
wv.plot("simulation.raw", "plot_config.yaml")

# Return figure for further customization
fig = wv.plot("simulation.raw", "plot_config.yaml", show=False)
fig.update_layout(title="Custom Title")
fig.show()

# Inline configuration (no YAML file needed)
wv.plot("simulation.raw", config={
    "X": {"signal_key": "raw.time", "label": "Time (s)"},
    "Y": [{"label": "Voltage (V)", "signals": {"VDD": "v(vdd)"}}]
})
```

### Advanced API (power users)
```python
import wave_view as wv

# Explore available signals
data = wv.load_spice("simulation.raw")
print(data.signals)  # List all available signals
print(data.info)     # File info, simulation type, etc.

# Advanced plotter with signal processing
plotter = wv.SpicePlotter("simulation.raw")
plotter.add_processed_signal("power", lambda d: d["v(vdd)"] * d["i(vdd)"])
plotter.load_config("config.yaml")
fig = plotter.create_figure()
fig.show()

# Batch plotting
wv.plot_batch([
    ("sim1.raw", "config1.yaml"),
    ("sim2.raw", "config2.yaml")
], layout="grid")
```

### Configuration Helpers
```python
# Generate template configurations
wv.create_config_template("my_config.yaml", signals=["v(vdd)", "v(out)", "i(vdd)"])

# Validate configuration
wv.validate_config("config.yaml", "simulation.raw")

# Interactive config builder (for Jupyter)
builder = wv.ConfigBuilder("simulation.raw")
builder.add_voltage_plot(["v(vdd)", "v(out)"])
builder.add_current_plot(["i(vdd)"], separate_axis=True)
builder.save("generated_config.yaml")
```

## Core Classes

### 1. `SpiceData` (reader.py)
```python
class SpiceData:
    def __init__(self, raw_file_path: str)
    
    @property
    def signals(self) -> List[str]
    @property
    def time(self) -> np.ndarray
    @property
    def info(self) -> Dict[str, Any]
    
    def get_signal(self, name: str) -> np.ndarray
    def get_signals(self, names: List[str]) -> Dict[str, np.ndarray]
```

### 2. `PlotConfig` (config.py)
```python
class PlotConfig:
    def __init__(self, config_source: Union[str, Dict])
    
    def validate(self, spice_data: SpiceData) -> List[str]  # Returns warnings
    def to_dict(self) -> Dict
    
    @classmethod
    def from_template(cls, template_name: str) -> 'PlotConfig'
```

### 3. `SpicePlotter` (plotter.py)
```python
class SpicePlotter:
    def __init__(self, raw_file: str = None)
    
    def load_data(self, raw_file: str) -> 'SpicePlotter'
    def load_config(self, config: Union[str, Dict]) -> 'SpicePlotter'
    def add_processed_signal(self, name: str, func: Callable) -> 'SpicePlotter'
    def create_figure(self) -> plotly.graph_objects.Figure
    def show(self) -> None
```

## Main API Functions (\_\_init\_\_.py)

```python
# Simple plotting
def plot(raw_file: str, 
         config: Union[str, Dict] = None,
         show: bool = True,
         **kwargs) -> plotly.graph_objects.Figure

# Data loading
def load_spice(raw_file: str) -> SpiceData

# Configuration utilities
def create_config_template(output_path: str, 
                          raw_file: str = None,
                          signals: List[str] = None) -> None

def validate_config(config: Union[str, Dict], 
                   raw_file: str = None) -> List[str]

# Advanced plotting
def plot_batch(files_and_configs: List[Tuple[str, str]], 
               layout: str = "separate") -> List[plotly.graph_objects.Figure]
```

## Jupyter Notebook Integration

```python
# Auto-configuration based on common patterns
wv.quick_plot("simulation.raw")  # Auto-detects voltage/current signals

# Interactive widgets (if ipywidgets available)
wv.interactive_plot("simulation.raw")  # Creates interactive config widgets

# Export capabilities
wv.plot("sim.raw", "config.yaml").export("plot.html")
wv.plot("sim.raw", "config.yaml").export("plot.png", width=1200, height=800)
```

## Example Usage Scenarios

### Scenario 1: Quick Exploration
```python
import wave_view as wv

# Auto-plot with sensible defaults
wv.quick_plot("my_simulation.raw")

# See what signals are available
data = wv.load_spice("my_simulation.raw")
print(data.signals)
```

### Scenario 2: Custom Analysis
```python
import wave_view as wv

# Load data
plotter = wv.SpicePlotter("amplifier.raw")

# Add custom calculations
plotter.add_processed_signal("gain", 
    lambda d: 20 * np.log10(np.abs(d["v(out)"] / d["v(in)"])))

# Configure plot
config = {
    "title": "Amplifier Analysis",
    "X": {"signal_key": "raw.freq", "label": "Frequency (Hz)"},
    "Y": [
        {"label": "Gain (dB)", "signals": {"Gain": "data.gain"}},
        {"label": "Phase (deg)", "signals": {"Phase": "phase(v(out)/v(in))"}}
    ]
}
plotter.load_config(config)
plotter.show()
```

### Scenario 3: Batch Processing
```python
import wave_view as wv

# Process multiple simulations
corners = ["tt", "ss", "ff"]
for corner in corners:
    wv.plot(f"sim_{corner}.raw", "config.yaml").export(f"plot_{corner}.html")
```

## Key Design Decisions

1. **Simple by default, powerful when needed**: Basic `plot()` function for 90% of cases
2. **Fluent API**: Method chaining for advanced use cases
3. **Jupyter-first**: Auto-display, good error messages, interactive widgets
4. **Flexible configuration**: YAML files, Python dicts, or programmatic building
5. **Extensible**: Easy to add custom signal processing
6. **Type hints**: Full type annotation for better IDE support

## Multi-Figure Configuration Support

The package will support both single-figure and multi-figure configuration files:

### Single Figure Config (existing format)
```yaml
title: "Ring Oscillator Analysis"
source: "./sim.raw"
X:
  label: "Time (s)"
  signal_key: "raw.time"
Y:
  - label: "Voltage (V)"
    signals:
      VDD: "v(vdd)"
```

### Multi-Figure Config (list format)
```yaml
- title: "Figure 1"
  source: "./sim1.raw"
  X: ...
  Y: ...
- title: "Figure 2"
  source: "./sim2.raw"
  X: ...
  Y: ...
```

### API Support for Both Formats
```python
# Single figure
wv.plot("sim.raw", "single_config.yaml")

# Multi-figure (returns list of figures)
figures = wv.plot_multi("multi_config.yaml")

# Multi-figure with subplot layout
wv.plot_multi("multi_config.yaml", layout="subplot")
``` 