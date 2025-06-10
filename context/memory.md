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
- **Test Coverage**: ✅ **ALL TESTS PASSING**: 226 passing, 0 failing (100% pass rate)
- **API Coverage**: 87% with comprehensive validation
- **Overall Coverage**: 92% with comprehensive test suite
- **Repository Structure**: Modern src/ layout ready for PyPI publication

### **Core Modules Status**
- **SpiceData (reader.py)**: 100% coverage, case-insensitive signal access
- **PlotConfig (config.py)**: 96% coverage, YAML configuration system
- **SpicePlotter (plotter.py)**: 95% coverage, advanced Plotly integration
- **API (api.py)**: 87% coverage, comprehensive input validation

### **Key API Functions**
- `plot()` - Main plotting function with required config parameter
- `load_spice()` - SPICE file loading with Path object support
- `explore_signals()` - Signal discovery with categorized output
- `validate_config()` - Configuration validation with helpful warnings
- `config_from_file()` - Load configuration from YAML files
- `config_from_yaml()` - Create configuration from YAML strings

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

## API Changes Successfully Implemented ✅

### **Explicit Configuration API**
- **Removed auto-detection**: PlotConfig constructor only accepts Path, dict, or list
- **Added factory functions**: `config_from_file()`, `config_from_yaml()`, `config_from_dict()`
- **Simplified API surface**: Removed `plot_batch()` function
- **Enhanced type safety**: Proper isinstance() checks and type validation

### **Test Fixes Completed** ✅
All 23 failing tests have been successfully fixed:

1. **PlotConfig Constructor Tests** (11 tests) - Updated to use factory functions
2. **plot() Function API Tests** (4 tests) - Updated mock expectations for PlotConfig objects
3. **plot_batch Tests** (8 tests) - Removed entire test file as function was deleted
4. **Internal Method Tests** (4 tests) - Removed TestFilePathDetection class
5. **Type Import Issues** (1 test) - Fixed isinstance() checks with proper imports

### **Key Changes Made**
- Updated all tests to use `config_from_file()` instead of passing file paths to PlotConfig
- Updated all tests to use `config_from_yaml()` instead of passing YAML strings to PlotConfig
- Fixed mock expectations to expect PlotConfig objects instead of dictionaries
- Removed tests for deprecated auto-detection functionality
- Fixed isinstance() type checking issues in path support tests

## Current Issues Identified
1. **Signal categorization logic duplication** in `explore_signals()` (api.py:285-300)
2. **Magic numbers** in error messages (reader.py:95-96) - hardcoded `[:5]`
3. **Missing type annotations** on internal functions (api.py:145-166)
4. **Error message enhancement opportunity** for signal name suggestions (reader.py:97-101)

## Open Questions
None - package is functionally complete with all tests passing. Ready for code quality polish before publication.

## Next Steps
1. **Code Quality Polish**: Extract utilities, replace magic numbers, add type annotations
2. **Documentation**: Standardize docstring examples
3. **Publication Preparation**: Polish README, set up CI/CD, prepare for PyPI
