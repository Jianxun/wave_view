# Wave_view Architecture Decisions

## Overview
This document captures key architectural decisions for wave_view v0.2.0 and beyond, based on comprehensive API improvement analysis and user feedback.

## Current Architecture (v0.1.0)

### Core Components
- **SpiceData (reader.py)**: Wraps spicelib.RawRead, normalizes signal names, lazy signal access
- **PlotConfig (config.py)**: YAML/Dict configuration loading and validation
- **SpicePlotter (plotter.py)**: Plotly figure generation with multi-axis support
- **API (api.py)**: Top-level functions (`plot`, `load_spice`, `explore_signals`)

### Current Workflow
```python
# Step 1: Discovery
signals = wv.explore_signals("simulation.raw")

# Step 2: Configuration  
config = wv.config_from_yaml("...")

# Step 3: Plotting
fig = wv.plot("simulation.raw", config)
```

### Strengths
- Interactive Plotly visuals
- Case-insensitive signal handling
- Processed signal hooks
- Comprehensive validation

### Limitations
- File parsed multiple times for multiple plots
- Single-figure API limits composability
- No schema validation for configurations
- Tight coupling to spicelib
- No multi-file parameter sweep support

## Architecture Evolution for v0.2.0

### Design Principles
1. **Composability over Convenience**: Enable complex workflows while maintaining simple cases
2. **Efficiency**: Parse files once, reuse for multiple visualizations
3. **Extensibility**: Support future features without breaking existing code
4. **Backward Compatibility**: Maintain existing API as convenience layer

### Key Architectural Changes

#### 1. PlotSpec-Based API (Core Refactoring)

**Current API:**
```python
fig = wv.plot("sim.raw", config)
```

**New API:**
```python
data = wv.load_spice("sim.raw")
spec = wv.PlotSpec(config)
spec.plot(data).show()
fig = spec.get_figure()
```

**Benefits:**
- Parse file once, reuse for multiple plots
- Fluent API with method chaining
- Better separation of concerns
- Extensible for future features

#### 2. Enhanced Data Layer

**WaveDataset Class:**
```python
class WaveDataset:
    signals: Dict[str, np.ndarray]
    meta: Dict[str, Any]  # temperature, corner, vdd, etc.
    
    @classmethod
    def from_raw(cls, path: str, meta: Dict = None) -> 'WaveDataset'
```

**Benefits:**
- Self-describing data with metadata
- Foundation for parameter sweep support
- Consistent interface across single/multi-file workflows

#### 3. Pydantic Configuration Models

**Replace ad-hoc validation with structured models:**
```python
class PlotSpec(BaseModel):
    x: str
    y: List[str]
    style: Optional[Dict]
    title: Optional[str]
    
    @classmethod
    def from_yaml(cls, yaml_str: str) -> 'PlotSpec'
```

**Benefits:**
- JSON Schema generation for editor support
- Rich error messages with line numbers
- Type safety and autocompletion
- Programmatic configuration composition

#### 4. Pluggable Reader Architecture

**Abstract reader interface:**
```python
class Reader(ABC):
    @abstractmethod
    def load(self, path: str) -> WaveDataset
    
class SpiceRawReader(Reader):
    # Current spicelib implementation
    
class NgSpiceCSVReader(Reader):
    # Future CSV support
```

**Benefits:**
- Support multiple simulation formats
- Easier testing with mock readers
- Future-proofing for new formats

## HTML Report Builder Architecture

### ReportSpec Configuration
```yaml
title: "OTA PVT Sweep Analysis"
author: "Dr. Jianxun Zhu"
theme: "dark"

sections:
  - heading: "DC Transfer Curves"
    notes: "Linearity spec: ±1%"
    figures:
      - spec: dc_transfer.yaml
        dataset: sim.raw
        
  - heading: "AC Response vs Temperature"
    slice: {corner: tt}
    group: [temperature]
    legend: "tt_{temperature}°C"
    spec: ac_bode.yaml
```

### Implementation Components
1. **ReportSpec (Pydantic)**: Declarative report configuration
2. **ReportBuilder**: Jinja2 template system for HTML generation
3. **CLI Interface**: `wave_view report report.yaml --out report.html`

### HTML Data Storage
- **Self-contained**: All data embedded as JSON in `<script>` tags
- **Plotly Integration**: `fig.to_html(include_plotlyjs="cdn|inline")`
- **Size Management**: Decimation options for large datasets

## Parameter Sweep Architecture (v0.3.0)

### Metadata-as-DataFrame Approach
```python
# Metadata table
meta_df = pd.DataFrame([
    {"case": 0, "path": "sim/0.raw", "temperature": 25, "corner": "tt"},
    {"case": 1, "path": "sim/1.raw", "temperature": 85, "corner": "tt"},
    # ...
])

# Operations
filtered = slice_df(meta_df, {"temperature": 85})
grouped = group_df(filtered, ["temperature", "corner"])
```

### Configuration Format
```yaml
slice:                    # Filter data
  temperature: 85
  corner: tt

group:                    # Group traces
  - temperature
  - corner

legend: "{corner}_{temperature}°C"    # Template

aggregator: envelope      # Statistical processing
```

### Multi-File Collection
```python
class WaveDataCollection:
    def __init__(self, sources: Union[List[str], Dict[str, str]])
    def get_signal(self, name: str) -> Dict[str, np.ndarray]
    def validate_compatibility(self) -> List[str]
```

## Implementation Phases

### Phase 1: Core API Refactoring (v0.2.0)
- [ ] PlotSpec class with Pydantic validation
- [ ] SpicePlotter accepts SpiceData objects
- [ ] Backward compatibility wrapper
- [ ] Enhanced configuration validation

### Phase 2: HTML Report Builder (v0.2.0)
- [ ] ReportSpec Pydantic model
- [ ] ReportBuilder with Jinja2 templates
- [ ] CLI command implementation
- [ ] Self-contained HTML generation

### Phase 3: Parameter Sweep Foundation (v0.2.0)
- [ ] WaveDataset with metadata support
- [ ] DataFrame-based filtering/grouping
- [ ] Legend templating system
- [ ] Multi-file preparation

### Phase 4: Full Parameter Sweep Engine (v0.3.0)
- [ ] WaveDataCollection class
- [ ] Statistical aggregators
- [ ] Advanced sweep visualization
- [ ] Monte Carlo analysis support

## Design Decisions

### 1. Pydantic vs JSON Schema
**Decision**: Use Pydantic for configuration models
**Rationale**: Better Python integration, automatic JSON Schema generation, rich error messages

### 2. Backward Compatibility Strategy
**Decision**: Maintain existing `wv.plot()` as convenience wrapper
**Rationale**: Avoid breaking existing user code while enabling new capabilities

### 3. HTML Report Priority
**Decision**: Prioritize HTML reports over parameter sweeps
**Rationale**: More immediate user value, simpler implementation, foundation for sweeps

### 4. Self-Contained HTML
**Decision**: Embed all data as JSON in HTML files
**Rationale**: Simplifies sharing, works offline, integrates with Obsidian workflow

### 5. DataFrame for Metadata
**Decision**: Use pandas DataFrame for parameter sweep metadata
**Rationale**: Mature ecosystem, familiar operations, efficient filtering/grouping

## Migration Strategy

### For v0.1.0 Users
1. **Existing code continues to work** - no breaking changes
2. **Gradual migration path** - can adopt new API incrementally
3. **Clear documentation** - migration guide with examples
4. **Deprecation warnings** - for features being phased out

### For New Users
1. **Promote new API** in documentation
2. **Show both patterns** in examples
3. **Emphasize benefits** of new approach
4. **Provide templates** for common use cases

## Testing Strategy

### Test Data Requirements
1. **Parameter sweep dataset**: PVT corners with metadata
2. **Multi-analysis dataset**: Same circuit, different analyses
3. **Large file dataset**: Performance testing
4. **Edge case dataset**: Error handling validation

### Test Organization
1. **Unit tests**: Individual components
2. **Integration tests**: End-to-end workflows
3. **Performance tests**: Large file handling
4. **Regression tests**: Backward compatibility

## Future Considerations

### Potential Extensions
1. **Interactive dashboards**: Jupyter widgets integration
2. **Streaming support**: Very large file handling
3. **Cloud integration**: Remote file access
4. **Plugin system**: Custom readers and processors

### Scalability Concerns
1. **Memory usage**: Large parameter sweeps
2. **File I/O**: Concurrent raw file access
3. **HTML size**: Many figures in reports
4. **Browser performance**: Complex interactive plots

## Success Metrics

### Developer Experience
- Reduced lines of code for common tasks
- Faster development iteration
- Better error messages and debugging

### Performance
- Single file parse for multiple plots
- Efficient parameter sweep processing
- Reasonable HTML report sizes

### Adoption
- Backward compatibility maintained
- New features actively used
- Positive user feedback

---

*This document will be updated as architecture decisions are implemented and refined.* 