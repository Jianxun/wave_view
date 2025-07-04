# Wave View v1.0.0 Architecture

## Overview
This document outlines the major architectural decisions for Wave View v1.0.0, representing a significant API simplification and refactoring from the current v0.2.0 implementation.

## Core Principles

### 1. Separation of Concerns
- **PlotSpec**: Pure configuration validation and management
- **Plotting Functions**: Pure visualization behavior
- **Data Preparation**: Standalone signal processing (future implementation)

### 2. Simple Interfaces
- Prefer `Dict[str, np.ndarray]` over complex data objects
- Direct signal name lookup instead of resolution logic
- Function-based API for extensibility

### 3. Future Extensibility
- Support for multi-case plotting (PVT, Monte Carlo, parameter sweeps)
- Modular design allows adding new plot types without core changes

## Major API Changes

### PlotSpec Simplification

**Before (v0.2.0):**
```python
def plot(self, data, processed_data: Optional[Dict[str, np.ndarray]] = None) -> go.Figure:
    # data: SpiceData object
    # processed_data: Optional processed signals dictionary
```

**After (v1.0.0):**
```python
# PlotSpec becomes configuration-only
class PlotSpec:
    @classmethod
    def from_yaml(cls, yaml_str: str) -> 'PlotSpec'
    
    @classmethod  
    def from_file(cls, file_path: Path) -> 'PlotSpec'
    
    # NO plotting methods - just configuration
```

### Function-Based Plotting API

**Primary API (v1.0.0):**
```python
# Single-case plotting
spec = wv.PlotSpec.from_yaml(config)
fig = wv.plot(data=data, spec=spec)
fig.show()

# Future multi-case plotting
fig_multi = wv.plot_multi_case(multi_case_data, sweep_meta_data, spec)
fig_pvt = wv.plot_pvt_corners(pvt_data, corner_info, spec)
fig_monte = wv.plot_monte_carlo(mc_data, stats_info, spec)
```

## Signal Resolution Changes

### Direct Signal Lookup

**Before:** Complex signal resolution with prefixes
```python
# Config supports prefixes like "raw.frequency" vs "frequency"
# PlotSpec handles signal resolution logic
```

**After:** Direct dictionary lookup
```python
# YAML config uses exact signal names
x: "time"
y:
  - label: "Output Voltage"
    signals:
      "V_out": "v(out)"  # Must exist exactly as "v(out)" in data dict
```

### Benefits
- Eliminates complex resolution logic
- Clear 1:1 mapping between config and data
- Easier to debug and test
- Simpler implementation

## Plotter Refactoring

### Standalone Functions

**New Plotter Architecture:**
```python
def create_plot(data: Dict[str, np.ndarray], config: dict) -> go.Figure:
    """
    Create figure from data and configuration.
    
    Args:
        data: Signal name → numpy array mapping
        config: Plot configuration dict
    """
    # 1. Create base figure
    fig = create_figure()
    
    # 2. Setup layout (axes, title, controls)  
    layout = create_layout(config)
    fig.update_layout(layout)
    
    # 3. Add waveforms
    x_signal = config["x"]
    x_data = data[x_signal]  # Direct lookup
    
    for y_spec in config["y"]:
        for legend_name, signal_key in y_spec["signals"].items():
            y_data = data[signal_key]  # Direct lookup
            add_waveform(fig, x_data, y_data, name=legend_name, ...)
    
    return fig
```

### Helper Functions
```python
def create_figure() -> go.Figure:
    """Create empty figure with basic setup."""

def create_layout(config: dict) -> dict:
    """Create layout configuration for multiple Y-axes, controls, etc."""

def add_waveform(fig: go.Figure, x_data: np.ndarray, y_data: np.ndarray, 
                legend: str, y_axis: str = "y1", **style) -> None:
    """Add single waveform trace to figure."""
```

## Interface Design

### PlotSpec ↔ Plotter Interface

**Simple and Clean:**
```python
# PlotSpec converts to simple dict
config = spec._to_config()  # Returns plain dict

# Plotter takes simple inputs
fig = create_plot(data, config)
```

**No Complex Dependencies:**
- Plotter doesn't know about SpiceData, processed signals, etc.
- Direct `Dict[str, np.ndarray]` + `dict` → `go.Figure`
- Easy to test with simple dictionary inputs

## Data Preparation (Future)

### Deferred Implementation
- Lambda expressions for signal processing
- Standalone processor transparent to plotter
- Can be inserted later without changing PlotSpec/Plotter APIs

### Planned Approach
```python
# Future data preparation layer
raw_data = load_spice("file.raw")
processed = {"custom": lambda signals: ...}
data = prepare_plot_data(raw_data, processed)  # → Dict[str, np.ndarray]
```

## Benefits of This Architecture

### 1. Simplicity
- PlotSpec focuses purely on configuration
- Plotter handles only visualization
- Clear separation of responsibilities

### 2. Testability
- Easy to test with simple dictionary inputs
- No complex mock objects needed
- Clear input/output contracts

### 3. Extensibility
- Add new plot types without touching PlotSpec
- Consistent pattern: `plot_**(data, spec)`
- Future multi-case plotting naturally supported

### 4. Performance
- Direct dictionary lookup vs complex resolution
- No unnecessary data conversions
- Minimal object creation

## Migration Strategy

### Breaking Changes
- PlotSpec.plot() method removed
- New function-based API required
- Signal resolution logic simplified

### Backward Compatibility
- Maintain convenience wrappers where possible
- Clear migration guide for users
- Version bump to v1.0.0 to signal breaking changes

## Implementation Phases

### Phase 1: Core API Refactoring
1. Refactor PlotSpec to remove plotting methods
2. Implement standalone plotting functions
3. Update plotter to use Dict[str, np.ndarray] interface
4. Remove signal resolution logic

### Phase 2: Data Preparation Layer
1. Design lambda-based signal processing
2. Create standalone data preparation utilities
3. Implement backward compatibility wrappers

### Phase 3: Multi-Case Foundation
1. Design multi-case data structures
2. Implement plot_multi_case() function
3. Add metadata handling for parameter sweeps

## Decision Rationale

### Why Function-Based Over Method-Based?

**Method-based would lead to:**
```python
# Becomes unwieldy with many plot types
spec.plot(data)
spec.plot_multi_case(multi_data, meta)
spec.plot_pvt_corners(pvt_data, corners)
spec.plot_monte_carlo(mc_data, stats)
```

**Function-based is cleaner:**
```python
# Consistent pattern, easy to extend
wv.plot(data, spec)
wv.plot_multi_case(multi_data, meta, spec)
wv.plot_pvt_corners(pvt_data, corners, spec)
wv.plot_monte_carlo(mc_data, stats, spec)
```

### Why Dict[str, np.ndarray] Over Complex Objects?

- **Simplicity**: No need to understand SpiceData internals
- **Flexibility**: Users can construct from any data source
- **Performance**: Direct array access, no object overhead
- **Testability**: Easy to create test data dictionaries

## Conclusion

This v1.0.0 architecture represents a significant simplification that:
- Reduces complexity in core components
- Provides clear separation of concerns
- Enables future extensibility for multi-case plotting
- Maintains high performance and testability

The breaking changes are justified by the long-term benefits of a cleaner, more maintainable architecture. 