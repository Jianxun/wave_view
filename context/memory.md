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
- **Test Coverage**: ⚠️ **BREAKING**: 207 passing, 23 failing due to API changes
- **API Coverage**: 85% with comprehensive validation
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

## API Changes Breaking Tests
**23 tests failing due to explicit configuration API refactor:**

### **PlotConfig Constructor Changes** (11 tests)
- **Issue**: PlotConfig no longer accepts strings (YAML content or file paths)
- **Affected**: `test_config_basic.py` (8 tests), `test_basic.py` (2 tests), `test_config_features.py` (3 tests)
- **Root Cause**: Removed auto-detection logic, only accepts Path, dict, or list

### **plot() Function API Changes** (4 tests)
- **Issue**: plot() now requires PlotConfig objects or dicts, not file paths 
- **Affected**: `test_api_plot.py` (2 tests), `test_path_support.py` (2 tests)
- **Root Cause**: New explicit API requiring config_from_file() for YAML files

### **Missing Functions** (1 test file)
- **Issue**: plot_batch() function removed from API
- **Affected**: `test_plot_batch.py` (entire test file - 8 tests)
- **Root Cause**: Function removed to simplify API surface

### **Removed Methods** (4 tests)
- **Issue**: _looks_like_file_path() internal method removed
- **Affected**: `test_config_basic.py` TestFilePathDetection class
- **Root Cause**: Auto-detection logic removed from PlotConfig

### **Type Issues** (1 test)
- **Issue**: isinstance() call with invalid PlotConfig import
- **Affected**: `test_path_support.py::test_all_functions_accept_path_objects`
- **Root Cause**: Import/typing issue in api.py

## Current Issues Identified
1. **Signal categorization logic duplication** in `explore_signals()` (api.py:285-300)
2. **Magic numbers** in error messages (reader.py:95-96) - hardcoded `[:5]`
3. **Missing type annotations** on internal functions (api.py:145-166)
4. **Unimplemented grid layout** in `plot_batch()` (api.py:456-458) - **REMOVED**
5. **Error message enhancement opportunity** for signal name suggestions (reader.py:97-101)

## Open Questions
None - package is functionally complete and ready for code quality polish before publication.
