# Signal Discovery API Design

## Overview

The Signal Discovery API provides users with comprehensive tools to explore and understand the structure of SPICE raw files before creating visualizations. This addresses the common problem of users not knowing what signals are available or how they're named.

## Core Features

### 1. **Automatic Signal Categorization**
- **Voltage signals**: `V(node)` - Node voltages
- **Current signals**: `I(element)` - Element currents  
- **Device terminal signals**: `Ix(device:terminal)` - Device-specific currents
- **Time/Frequency axes**: Simulation independent variables
- **Other signals**: Uncategorized or special signals

### 2. **Rich Metadata Extraction**
- Signal names, types, units, and descriptions
- Device grouping for hierarchical organization
- File information (type, size, data points)
- Search and filtering capabilities

### 3. **Multiple Interface Options**
- **Command line**: Text-based exploration
- **Jupyter notebooks**: Rich HTML displays and interactive widgets
- **Programmatic**: Dictionary/DataFrame outputs for processing

## Proposed API

### Basic Signal Information

```python
import wave_view as wv

# Quick signal listing
data = wv.load_spice("simulation.raw")
print(data.signals)  # List all signal names
print(data.info)     # File metadata

# Get categorized signals  
signals = data.get_signals_by_type()
# Returns: {"voltage": [...], "current": [...], "device_terminal": [...]}
```

### Advanced Signal Explorer

```python
# Detailed signal exploration
explorer = wv.SpiceExplorer("simulation.raw")

# Rich display methods
explorer.show()                    # Auto-detects environment (Jupyter vs terminal)
explorer.display_summary()         # Text summary
explorer.display_tree()            # Hierarchical tree view

# Programmatic access
explorer.voltages                  # All voltage signals
explorer.currents                  # All current signals
explorer.devices                   # Device terminal signals grouped by device
explorer.search("vdd")             # Search for signals containing "vdd"
explorer.get_signal_info("V(vdd)") # Detailed info for specific signal
```

### Jupyter Integration

```python
# Interactive signal browser
browser = wv.browse_signals("simulation.raw")
browser.display_rich_summary()     # Rich HTML display with icons
browser.create_signal_selector()   # Interactive multi-select widget
browser.search_widget()            # Live search interface
browser.to_dataframe()             # Pandas DataFrame for analysis
```

### Configuration Helpers

```python
# Generate suggested configurations
config = wv.suggest_config("simulation.raw")
# Returns ready-to-use YAML configuration

# Interactive configuration builder  
builder = wv.ConfigBuilder("simulation.raw")
builder.add_voltage_plot(["V(vdd)", "V(out)"])
builder.add_current_plot(["I(vdd)"], separate_axis=True)
config = builder.get_config()

# Validate existing configuration
warnings = wv.validate_config("my_config.yaml", "simulation.raw")
```

## Example Usage Scenarios

### Scenario 1: First-time File Exploration

```python
import wave_view as wv

# Quick overview of what's in the file
explorer = wv.SpiceExplorer("new_simulation.raw")
explorer.show()

# Output:
# ============================================================
# SPICE Raw File Analysis: new_simulation.raw
# ============================================================
# File Type: Binary
# Variables: 66 | Data Points: 2,228 | Total Signals: 66
# 
# Signal Categories:
#   Time: 1        Voltage: 11       Current: 10
#   Device Terminal: 44
# 
# Voltage Signals:
#   V(vdd)     - Voltage at node vdd
#   V(out)     - Voltage at node out
#   V(bus01)   - Voltage at node bus01
#   ...
```

### Scenario 2: Finding Specific Signals

```python
# Search for power-related signals
power_signals = explorer.search("vdd")
print(f"Found {len(power_signals)} VDD-related signals")

# Find all transistor gate signals
gate_signals = explorer.search("gate", case_sensitive=False)

# Get all signals from a specific device
device_x4_signals = explorer.get_devices()["x4"]
```

### Scenario 3: Jupyter Notebook Discovery

```python
# In Jupyter notebook
import wave_view as wv

# Rich interactive exploration
browser = wv.browse_signals("amplifier.raw")

# This displays:
# 📊 SPICE Raw File Analysis
# File: amplifier.raw | Type: Binary | Signals: 45 | Data Points: 1,000
# 
# 📈 Signal Categories
# [Visual cards showing: ⏰ Time: 1, ⚡ Voltage: 12, 🔌 Current: 8, etc.]
#
# Interactive widgets for selection and search
```

### Scenario 4: Automated Configuration Generation

```python
# Generate intelligent configuration suggestions
config = wv.suggest_config("ring_oscillator.raw", max_signals=5)

# Output YAML:
# title: "SPICE Analysis - ring_oscillator.raw"
# source: "ring_oscillator.raw"
# X:
#   label: "Time (s)"
#   signal_key: "raw.time"
# Y:
#   - label: "Voltage (V)"
#     signals:
#       vdd: "v(vdd)"
#       out: "v(out)"
#       bus01: "v(bus01)"
```

## Implementation Architecture

### Core Classes

#### `SignalInfo` (Data Class)
```python
@dataclass
class SignalInfo:
    name: str           # Signal name (e.g., "V(vdd)")
    type: str           # Category: voltage, current, device_terminal, etc.
    units: str          # Physical units: V, A, s, Hz
    description: str    # Human-readable description
    device: str         # Device name (for device terminals)
    terminal: str       # Terminal name (for device terminals)
```

#### `SpiceSignalExplorer`
```python
class SpiceSignalExplorer:
    def __init__(self, raw_file_path: str)
    
    # Properties
    @property
    def file_info(self) -> Dict[str, Any]
    @property 
    def all_signals(self) -> List[SignalInfo]
    
    # Categorization methods
    def get_signals_by_type(self) -> Dict[str, List[SignalInfo]]
    def get_devices(self) -> Dict[str, List[SignalInfo]]
    
    # Search and filtering
    def search(self, query: str) -> List[SignalInfo]
    def get_signal_names(self, signal_type: str = None) -> List[str]
    
    # Display methods
    def display_summary(self)
    def display_tree(self)
```

#### `JupyterSignalBrowser`
```python
class JupyterSignalBrowser:
    def __init__(self, raw_file_path: str)
    
    # Rich display methods
    def display_rich_summary(self)              # HTML visualization
    def to_dataframe(self) -> pd.DataFrame      # Pandas integration
    
    # Interactive widgets
    def create_signal_selector(self) -> Widget  # Multi-select widget
    def search_widget(self) -> Widget           # Live search
```

## Signal Categorization Logic

The API uses intelligent pattern matching to categorize signals:

| Pattern | Type | Example | Description |
|---------|------|---------|-------------|
| `time` | time | `time` | Time axis for transient analysis |
| `V(node)` | voltage | `V(vdd)`, `V(out)` | Node voltages |
| `I(element)` | current | `I(R1)`, `I(V1)` | Element currents |
| `Ix(dev:term)` | device_terminal | `Ix(M1:GATE)` | Device terminal currents |
| `frequency` | frequency | `freq`, `f` | Frequency axis for AC analysis |

## Visualization Options

### 1. Text-Based (Terminal/Console)
- Structured summaries with categories
- Tree-like hierarchical display
- Search results with descriptions
- Device grouping with terminal lists

### 2. Rich HTML (Jupyter)
- Color-coded signal categories with icons
- Interactive expandable sections
- Visual file metadata cards
- Responsive layout for different screen sizes

### 3. Interactive Widgets (Jupyter)
- Multi-select signal chooser with live preview
- Search box with real-time filtering
- Configuration snippet generation
- Copy-to-clipboard functionality

### 4. Tabular (Pandas DataFrame)
- Sortable and filterable signal table
- Export capabilities (CSV, Excel)
- Integration with data analysis workflows
- Custom column selection

## Integration with Main API

The signal discovery features integrate seamlessly with the main plotting API:

```python
# Discover signals first
explorer = wv.SpiceExplorer("sim.raw")
voltages = explorer.get_signal_names("voltage")

# Use discovered signals in plotting
wv.plot("sim.raw", config={
    "X": {"signal_key": "raw.time", "label": "Time"},
    "Y": [{"label": "Voltages", "signals": {v: v.lower() for v in voltages[:3]}}]
})

# Or use suggested configuration
config = wv.suggest_config("sim.raw")
wv.plot("sim.raw", config=config)
```

## Benefits

1. **Reduced Learning Curve**: Users can immediately see what's available
2. **Error Prevention**: Reduces typos in signal names and configuration mistakes  
3. **Faster Workflow**: Quick discovery leads to faster plot creation
4. **Better Documentation**: Self-documenting files with rich metadata
5. **Intelligent Defaults**: Suggested configurations reduce manual work
6. **Cross-Platform**: Works in terminals, IDEs, and Jupyter notebooks

## Future Enhancements

- **Signal preview**: Quick waveform thumbnails
- **Unit detection**: Automatic unit inference from signal characteristics
- **Custom categorization**: User-defined signal grouping rules
- **Export capabilities**: Save signal lists and metadata
- **Integration with other tools**: Export to LTspice, Cadence formats 