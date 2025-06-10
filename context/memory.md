# Project Memory

## Project Overview
Wave_view is a Python package for SPICE simulation visualization with a modern, user-friendly API. The project features core modules for configuration management (config.py), data reading (reader.py), and plotting (plotter.py), with comprehensive YAML-based configuration support and advanced features like log scale plotting and processed signal generation.

## Current State

### **Architecture: Clean 3-Step Workflow**
```python
# Step 1: Discovery - "What's available?"
signals = wv.explore_signals("simulation.raw")

# Step 2: Configuration - "What do I want?"  
config = {...}  # Explicit user choices

# Step 3: Plotting - "Show me the results"
fig = wv.plot("simulation.raw", config)  # Required config, no magic
```

### **Package Status**
- **Installation**: `pip install -e .` (development mode)
- **Test Coverage**: 236 tests passing, 92% overall coverage
- **API Coverage**: 88% with comprehensive validation
- **Repository Structure**: Modern src/ layout ready for PyPI publication

### **Core Modules Status**
- **SpiceData (reader.py)**: 100% coverage, case-insensitive signal access
- **PlotConfig (config.py)**: 96% coverage, YAML configuration system
- **SpicePlotter (plotter.py)**: 95% coverage, advanced Plotly integration
- **API (api.py)**: 88% coverage, comprehensive input validation

### **Key API Functions**
- `plot()` - Main plotting function with required config parameter
- `load_spice()` - SPICE file loading with Path object support
- `explore_signals()` - Signal discovery with categorized output
- `validate_config()` - Configuration validation with helpful warnings
- `plot_batch()` - Batch plotting with configurable error handling

## Key Decisions

### **API Design Philosophy**
- **Explicit over implicit**: No hidden magic, all behavior transparent
- **Path object support**: Modern pathlib integration throughout
- **Comprehensive validation**: Clear error messages guide users
- **Test-driven development**: All features have comprehensive test coverage

### **Configuration System**
- **YAML-based**: Flexible configuration with file, string, or dict input
- **Multi-figure support**: Single config can define multiple plots
- **Processed data integration**: Users can pass computed signals via `processed_data` parameter
- **Log scale support**: Both X and Y axes support logarithmic scaling

### **Signal Handling**
- **Case-insensitive**: All signal names normalized to lowercase
- **Signal categorization**: Voltage (v()), current (i()), and other signals
- **Path objects**: Consistent Union[str, Path] support across all functions

## Current Issues Identified
1. **Signal categorization logic duplication** in `explore_signals()` (api.py:285-300)
2. **Magic numbers** in error messages (reader.py:95-96) - hardcoded `[:5]`
3. **Missing type annotations** on internal functions (api.py:145-166)
4. **Unimplemented grid layout** in `plot_batch()` (api.py:456-458)
5. **Error message enhancement opportunity** for signal name suggestions (reader.py:97-101)

## Open Questions
None - package is functionally complete and ready for code quality polish before publication.
