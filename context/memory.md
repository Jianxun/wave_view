# Project Memory

## Project Overview
Wave_view is a Python package for SPICE simulation visualization with a modern, user-friendly API. The project features core modules for configuration management (config.py), data reading (reader.py), and plotting (plotter.py), with comprehensive YAML-based configuration support and advanced features like log scale plotting and processed signal generation.

## Current State
**API Testing & Improvement Sprint - IN PROGRESS** 🚧

**🎯 CURRENT FOCUS**: Building comprehensive API tests and improving code quality

**API Testing Progress**:
- **API Test Infrastructure**: Complete shared utilities and fixtures ✅
- **plot() Function Tests**: 4 comprehensive tests covering basic functionality, show behavior, processed data, and auto-configuration ✅
- **Coverage**: API coverage increased from 20% to 25% ✅
- **Development Guidelines**: Enhanced with incremental testing, error handling, and API design principles ✅

**🎯 CRITICAL API IMPROVEMENTS - COMPLETE** ✅

**Following Focused Development Guidelines**: Successfully completed ALL critical priority API improvements using test-driven, incremental development:

### ✅ **Feature 1: File Path Validation** (COMPLETE)
- **Implementation**: Added comprehensive input validation for `raw_file` parameter in `plot()`
- **Error Handling**: User-friendly error messages for None, empty strings, non-string/Path types, and non-existent files
- **Path Support**: Consistent handling of both string and Path objects with proper conversion
- **Tests**: 3 comprehensive test cases covering all error scenarios
- **Result**: Clear TypeError/ValueError/FileNotFoundError with descriptive messages

### ✅ **Feature 2: Unused **kwargs Removal** (COMPLETE)  
- **Problem**: `**kwargs` parameter was silently ignored, causing confusion for users
- **Solution**: Removed unused `**kwargs` parameter completely from `plot()` function
- **API Clarity**: Function signature now only includes supported parameters
- **Error Handling**: Users get proper TypeError for unexpected keyword arguments
- **Tests**: 1 test case verifying proper error handling for unexpected parameters
- **Result**: Clean API with clear error messages for unsupported parameters

### ✅ **Feature 3: Processed Data Validation** (COMPLETE)
- **Implementation**: Added comprehensive validation for `processed_data` parameter types
- **Validation Logic**: Ensures dictionary with string keys and array-like (non-string) values
- **Error Messages**: Specific error messages identifying the exact validation failure
- **Tests**: 2 test cases covering non-dict input and invalid value types
- **Result**: Clear TypeError with guidance on correct data types and formats

### ✅ **Feature 4: plot_batch() Error Handling Enhancement** (COMPLETE)
- **Problem**: Silent failures with only console prints, poor error visibility
- **Solution**: Added configurable error handling with structured error information
- **Error Modes**: "collect" (default), "raise", "skip" (legacy behavior)
- **Return Enhancement**: `Union[List[go.Figure], Tuple[List[go.Figure], List[Dict[str, str]]]]`
- **Error Structure**: Dictionary with 'file', 'config', 'error' keys for detailed reporting
- **Tests**: 6 comprehensive test cases covering all error handling modes
- **Result**: Professional error handling with backward compatibility

### ✅ **Feature 5: Comprehensive Path Object Support** (COMPLETE)
- **Implementation**: Added `Union[str, Path]` support to all API functions
- **Functions Enhanced**: `plot()`, `load_spice()`, `create_config_template()`, `validate_config()`
- **Validation Pattern**: Consistent input validation with Path conversion for internal processing
- **User Experience**: Users can naturally use either strings or Path objects
- **Modern Standards**: Following Python 3.4+ pathlib best practices
- **Tests**: 9 comprehensive test cases covering Path support and validation
- **Result**: User-friendly API supporting both traditional strings and modern Path objects

**Development Process Excellence**:
- ✅ **Test-First Development**: Created failing tests before implementing each feature
- ✅ **Incremental Implementation**: One focused feature at a time with immediate verification
- ✅ **Immediate Testing**: Ran specific test cases after each implementation
- ✅ **Regression Prevention**: Verified all existing tests continue to pass
- ✅ **User-Friendly Errors**: All error messages guide users toward correct usage

**API Quality Improvements Achieved**:
- **Input Validation**: Comprehensive validation with clear error messages across all functions
- **API Clarity**: Removed confusing unused parameters and ensured consistent interfaces
- **Error Handling**: Professional error handling with configurable modes and structured information  
- **Path Support**: Modern pathlib integration throughout the entire API
- **User Experience**: Clear guidance and flexible input types for excellent developer experience
- **Test Coverage**: Increased from 20% to **79%** with comprehensive validation testing

**API Code Quality Analysis - COMPLETED** 📋

**Comprehensive analysis of `src/wave_view/api.py` identified multiple improvement areas:**

### 🔴 Critical Issues (High Priority)
1. **Error Handling & User Experience**:
   - Missing file path validation for `raw_file` parameter
   - Generic exception handling with poor user feedback
   - Silent failures in `plot_batch()` with only console prints
   - No input validation for `processed_data` types

2. **API Design Issues**:
   - Unused `**kwargs` parameter in `plot()` function (undocumented/unimplemented)
   - Inconsistent return types across functions
   - Mixed string/Path object support inconsistencies

### 🟡 Code Quality Issues (Medium Priority)
3. **Type Hints & Documentation**:
   - Missing type annotations on internal functions
   - Inconsistent docstring quality and examples
   - Unfinished TODO comments in auto-configuration

4. **Code Organization**:
   - Long functions (create_config_template() 80+ lines)
   - Duplicated signal categorization logic
   - Magic numbers without explanation ([:5], [:3], [:2])

### 🟢 Specific Improvement Tasks (Planned)
- Input validation and error handling enhancement
- Remove unused `**kwargs` or implement/document proper usage
- Consistent Path object support throughout API
- Better exception handling with specific error types
- Extract common signal categorization logic into utilities
- Replace print statements with proper logging
- Add comprehensive input validation for all public functions
- Improve error messages to guide users toward solutions

**Test Suite Development Sprint - COMPREHENSIVE COMPLETION** ✅

**🏆 MAJOR MILESTONE ACHIEVED**: Complete test-driven development with modular architecture for all core modules!

**Final Test Coverage Results**:
- **PlotConfig**: 73 tests, 96% coverage ✅
- **SpicePlotter**: 47 tests, 93% coverage ✅  
- **SpiceData**: 56 tests, 100% coverage ✅
- **API Module**: 4 tests, 25% coverage (in progress) 🚧
- **🎯 TOTAL**: **180 comprehensive tests** with **95%+ coverage** on core modules

**Test Architecture Excellence - COMPLETE**:
- **Consistent Modular Organization**: All three core modules follow the same modular test pattern
- **Shared Utilities**: Common fixtures, mock creators, and assertion helpers in each module's `__init__.py`
- **Real-World Integration**: Tests with actual SPICE files alongside controlled mocking
- **Comprehensive Coverage**: Basic functionality, error handling, edge cases, and advanced features
- **Development Guidelines**: Following test-driven development principles throughout
- **Maintainability**: Focused test files make it easy to understand and extend tests

**Recently Completed - Config Test Modularization**:
Successfully broke down the large monolithic `test_config.py` (742 lines) into a clean modular structure:
- **`tests/unit_tests/config/`** directory with organized test files
- **`__init__.py`**: Comprehensive shared utilities (temp file creators, mock utilities, validation helpers)
- **`test_config_basic.py`**: Initialization and basic functionality (24 tests)
- **`test_config_validation.py`**: Configuration validation and error handling (33 tests)  
- **`test_config_features.py`**: Advanced features (templates, log scale, raw file paths) (16 tests)
- **Total**: 73 tests maintaining 96% coverage with improved organization

**Modular Test Pattern Established**:
All three core modules now follow the same excellent pattern:
```
tests/unit_tests/{module}/
├── __init__.py                 # Shared utilities & fixtures
├── test_{module}_basic.py      # Core functionality
├── test_{module}_*.py          # Feature-specific test files
└── test_{module}_edge_cases.py # Error handling & edge cases
```

**Key Achievements Completed**:
- ✅ **SpiceData Reader Module Testing** (56 tests, 100% coverage)
- ✅ **SpicePlotter Module Testing** (47 tests, 93% coverage)  
- ✅ **PlotConfig Module Testing** (73 tests, 96% coverage)
- ✅ **Real SPICE File Integration** with Ring_Oscillator_7stage.raw
- ✅ **Consistent Modular Test Structure** across all core modules
- ✅ **Advanced Feature Testing** (log scale, processed signals, multi-figure)
- ✅ **Test Organization Excellence** with maintainable, focused test files

**Next Phase**: Integration testing and API validation to ensure seamless system operation.

**✅ SPRINT 1 COMPLETE + MAJOR API ENHANCEMENTS COMPLETE**
- Core wave_view package fully implemented ✅
- Repository reorganized for PyPI publication ✅
- Modern Python packaging structure (src/ layout) ✅
- Package installable via pip install -e . ✅
- **NEW**: Processed data API with clean user interface ✅
- **NEW**: Log scale support for X and Y axes ✅
- **NEW**: Comprehensive unit tests for PlotConfig class (33 tests, 96% coverage) ✅
- **NEW**: Comprehensive modular unit tests for SpicePlotter class (47 tests, 93% coverage) ✅
- Core reader tests in progress ⏳

**Repository Structure:**
```
wave_view/
├── src/wave_view/           # Main package (src layout)
├── tests/                   # Consolidated test suite
├── examples/                # Demo scripts & notebooks
│   ├── data/               # Demo SPICE files
│   ├── scripts/            # Python demo scripts  
│   └── notebooks/          # Jupyter demos
├── docs/                   # Documentation
├── pyproject.toml          # Modern packaging config
├── LICENSE                 # MIT license
├── requirements-dev.txt    # Development dependencies
└── README.md              # Project documentation
```

## Key Decisions
- **Package Name**: `wave_view` (snake_case) following PEP 8 conventions
- **Structure**: src/ layout for professional Python packaging  
- **License**: MIT License for open source distribution
- **Build System**: setuptools with pyproject.toml (modern standard)
- **API Design**: Simple plot() function + advanced SpicePlotter class
- **Configuration**: YAML-based plotting configuration system
- **Case Handling**: Case-insensitive signal name matching

## Completed Features
**Core API:**
- `load_spice()` - Load SPICE files
- `plot()` - Simple plotting interface  
- `SpicePlotter` - Advanced plotting class
- `PlotConfig` - YAML configuration system
- `create_config_template()` - Auto-generate configs

**Key Capabilities:**
- Multi-figure plotting support
- Case-insensitive signal access
- Processed signal generation (lambda functions)
- YAML configuration validation
- Auto-configuration from SPICE files
- Plotly integration with Jupyter widgets

## Open Questions
None - package is ready for publication!

## API for Signal Discovery

**✅ Signal Exploration APIs Available:**

1. **Basic Signal Listing** (Core API):
   ```python
   data = wv.load_spice("file.raw")
   print(data.signals)  # List all signal names (lowercase)
   print(data.info)     # File metadata
   ```

2. **Advanced Signal Explorer** (Examples ready for integration):
   - `SpiceSignalExplorer` class in `examples/scripts/signal_explorer.py`
   - Categorizes signals by type (voltage, current, device terminals)
   - Provides display_summary(), display_tree(), search(), and categorization methods

3. **YAML Configuration Support**:
   - Full YAML string support for configurations (multi-line strings)
   - Multi-figure YAML configurations (list format)
   - Auto-template generation: `wv.create_config_template("output.yaml", raw_file="input.raw")`
   - YAML file loading and validation

**✅ NEW: Processed Data API (User-Facing)**

4. **Processed Data Parameter** (Main API Enhancement):
   ```python
   import wave_view as wv
   import numpy as np
   
   # Load data and compute processed signals
   data = wv.load_spice("simulation.raw")
   processed_data = {
       "vdb_out": 20 * np.log10(np.abs(data.get_signal("v(out)"))),
       "power": data.get_signal("v(vdd)") * data.get_signal("i(vdd)"),
       "phase": np.angle(data.get_signal("v(out)")) * 180 / np.pi
   }
   
   # Use in YAML config with "data." prefix
   config = '''
   title: "Analysis with Processed Data"
   X: {signal_key: "raw.time", label: "Time (s)"}
   Y:
     - label: "Magnitude (dB)"
       signals: {Output: "data.vdb_out"}
     - label: "Power (W)"
       signals: {Supply: "data.power"}
   '''
   
   # Plot with processed data
   fig = wv.plot("simulation.raw", config, processed_data=processed_data)
   ```

**Key Enhancement**: SpicePlotter is now internal-only. Users get clean API via `processed_data` parameter in the main `plot()` function.

**✅ NEW: Log Scale Support**

5. **Logarithmic Axis Scaling**:
   ```yaml
   # X-axis log scale (perfect for Bode plots)
   X:
     signal_key: "raw.frequency"
     label: "Frequency (Hz)"
     scale: log
   
   # Y-axis log scale (useful for power analysis)  
   Y:
     - label: "Power (W)"
       scale: log
       signals:
         Supply: "data.power"
   ```
   
   **Use Cases:**
   - Frequency response plots (Bode plots)
   - Power analysis with wide dynamic range
   - Any data spanning multiple orders of magnitude
   - Both X and Y axes support `scale: log` or `scale: linear` (default)

## Recent Issues Resolved
- **Import Issue Fixed**: Updated demo script to use proper package import (`import wave_view as wv`) instead of hacky sys.path manipulation
- **Package Installation**: Confirmed package is properly installed in development mode (pip install -e .)
- **X-Axis Positioning Fixed**: Fixed x-axis positioning by correcting Y-axis domain calculation and improving UX. All y-axes now properly anchor to x-axis with intuitive stacking order.
- **Y-Axis Order UX Fixed**: Reversed Y-axis processing order so first Y-axis in config appears at TOP of plot (intuitive reading order), not bottom. This matches user expectations.
- **Comprehensive Testing Added**: Created full test suite covering all API functionality, edge cases, and configuration formats
- **Documentation Updated**: Enhanced README.md with comprehensive installation instructions including development mode and GitHub installation options
- **API Enhancement - Processed Data**: Modified `plot()` function to accept `processed_data` parameter, eliminating need for users to access internal SpicePlotter class. Users can now pass pre-computed numpy arrays and reference them in YAML config with "data." prefix.
- **Log Scale Support**: Added logarithmic axis scaling for both X and Y axes. Users can specify `scale: log` in YAML configuration for frequency response plots (Bode plots) and other logarithmic data visualization.

## Next Steps
- Polish documentation for PyPI
- Consider GitHub Actions for CI/CD
- Plan Sprint 2 features (signal exploration UI) 