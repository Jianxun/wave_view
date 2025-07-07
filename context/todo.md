# Project Todo List

## Current Sprint - Version 1.0.0 Release Preparation 🚀 **ARCHITECTURE COMPLETE**

### 📋 **Engineering Notation Enhancement - COMPLETED** ✅ **FREQUENCY DOMAIN IMPROVEMENT**

#### **Automatic SI Prefix Detection** ✅ **COMPLETED**
- [X] **Enhanced frequency domain plotting** ✅ **COMPLETED**
  - Added automatic detection of frequency signals in X-axis configuration
  - Implemented SI engineering notation (1G, 1M, 1k) instead of American notation (1B, 1M, 1K)
  - Fixed Plotly exponentformat to "SI" for signals containing "frequency" in the name
  - Improves readability for AC analysis and frequency response plots
  
- [X] **Comprehensive test coverage** ✅ **COMPLETED**
  - Added tests for frequency signal detection with and without log scale
  - Added tests to ensure non-frequency signals use default formatting
  - All tests passing with 100% coverage of new functionality
  
- [X] **User experience improvement** ✅ **COMPLETED**
  - Automatic activation - no configuration required from users
  - Works with existing YAML specifications and PlotSpec configurations
  - Maintains backward compatibility for all existing plots

### 📋 **Legacy Code Removal - COMPLETED** ✅ **PURE v1.0.0 ARCHITECTURE**

#### **Phase 1.6: Legacy Reader Removal** ✅ **COMPLETED**
- [X] **Remove legacy reader.py file** ✅ **COMPLETED**
  - Deleted src/wave_view/core/reader.py completely
  - SpiceData class no longer exists in the package
  
- [X] **Update CLI to use v1.0.0 API** ✅ **COMPLETED**
  - Migrated CLI from SpiceData to WaveDataset
  - Updated CLI to use v1.0.0 plotting functions
  - Both `plot` and `signals` commands now use modern API
  
- [X] **Clean up package imports and exports** ✅ **COMPLETED**
  - Removed SpiceData from __init__.py exports
  - Removed all imports from reader module
  - Package now only exports modern v1.0.0 components
  
- [X] **Remove legacy reader tests** ✅ **COMPLETED**
  - Deleted entire tests/unit_tests/reader/ directory
  - Fixed test imports to remove SpiceData references
  - Cleaned up test dependencies

#### **API Cleanup Tasks** ✅ **COMPLETED** 🧹 **MAXIMUM SIMPLIFICATION SUCCESS**

#### **Function Removal for API Clarity** ✅ **COMPLETED**
- [X] **Remove `_categorize_signals()` function** ✅ **COMPLETED**
  - Too specific - users can infer signal types from naming conventions
  - Eliminates unnecessary complexity in signal exploration
  
- [X] **Remove `explore_signals()` function** ✅ **COMPLETED**
  - Users can directly examine data dictionary keys now
  - Redundant with `load_spice_raw()` approach
  
- [X] **Remove `load_spice()` legacy method** ✅ **COMPLETED**
  - Superseded by `load_spice_raw()` with cleaner Dict format
  - Eliminates SpiceData dependency from public API
  - Updated `__init__.py` to remove function exports

- [X] **Remove redundant `api.plot()` wrapper** ✅ **COMPLETED**
  - Expose `core.plotting.plot()` directly for maximum simplicity
  - Eliminates unnecessary file path handling and config conversion
  - Users now have explicit control: `load_spice_raw()` → `PlotSpec` → `plot()`
  - Cleaner data flow with single responsibility functions

### 📋 **v1.0.0 Implementation Status - COMPLETED** ✅ **MAJOR MILESTONE**

#### **Phase 1: Core API Refactoring** ✅ **COMPLETED**
- [X] **PlotSpec Simplification** ✅ **COMPLETED**
  - ✅ Remove plotting methods from PlotSpec class
  - ✅ Focus on configuration-only functionality  
  - ✅ Maintain factory methods (`from_yaml`, `from_file`)
  - ✅ Add clean `to_dict()` export method for v1.0.0 plotting functions
  - ✅ Archive v0.2.0 implementation in `src/wave_view/_archive/plotspec_v0_2_0.py`
  - ✅ Update tests using strict TDD methodology (6 tests passing, 88% coverage)
  
- [X] **Standalone Plotting Functions** ✅ **COMPLETED**
  - ✅ Create plotting.py module with function-based API
  - ✅ Implement helper functions: `create_figure()`, `create_layout()`, `add_waveform()`
  - ✅ Remove SpiceData dependency from plotting functions
  - ✅ Direct signal lookup without complex resolution
  - ✅ Multi-axis support with proper domain calculation
  - ✅ Full test coverage with integration tests (10 tests passing, 96% coverage)
  
- [X] **Code Quality Enhancement** ✅ **COMPLETED**
  - ✅ Refactor create_layout() function using single-responsibility principle
  - ✅ Extract 7 focused functions with clear responsibilities
  - ✅ Maintain 96% test coverage throughout refactoring process
  - ✅ Achieve 75% complexity reduction (127+ lines → 32 lines)
  
- [X] **Plotting Excellence** ✅ **COMPLETED**
  - ✅ Simplify zoom functionality - remove complex zoom buttons
  - ✅ Implement optimal zoom XY mode by default with `_config_zoom()` function
  - ✅ Fix Y-axis ordering so first axis appears at top (matching YAML order)
  - ✅ Resolve floating-point precision issues in multi-axis domain calculations
  - ✅ Improve user experience with intuitive zoom behavior
  
- [X] **Final API Migration** ✅ **COMPLETED**
  - ✅ Remove legacy plotter.py file completely
  - ✅ Replace plot_v1() with unified plot() function using v1.0.0 architecture
  - ✅ Clean up all SpicePlotter imports from __init__.py and api.py
  - ✅ Update demo to use clean wv.plot() API
  - ✅ Implement automatic renderer configuration on import
  - ✅ Achieve single elegant import: `import wave_view as wv`

- [X] **Legacy Config Removal** ✅ **COMPLETED**
  - ✅ Archive config.py as config_legacy.py in _archive/ directory
  - ✅ Remove PlotConfig class and all related functions from package
  - ✅ Remove config_from_file(), config_from_yaml(), validate_config() functions from api.py
  - ✅ Remove unused yaml import from api.py
  - ✅ Update plot() function to use PlotSpec.model_validate() for dict configs
  - ✅ Clean package namespace - only PlotSpec remains for configuration
  - ✅ Breaking change: 160 lines of legacy code removed (commit c9cb970)

- [X] **Legacy Reader Removal** ✅ **COMPLETED**
  - ✅ Remove reader.py file and SpiceData class completely
  - ✅ Update CLI to use WaveDataset and v1.0.0 plotting functions
  - ✅ Clean up package imports and exports
  - ✅ Remove legacy reader tests directory
  - ✅ Zero legacy code remains in the package

### 📋 **v1.0.0 Architecture - FULLY IMPLEMENTED** ✅ **SUCCESS**

#### **Clean v1.0.0 API Achieved** ✅ **PRODUCTION READY**
```python
import wave_view as wv

# Method 1: Direct plotting
spec = wv.PlotSpec.from_yaml("config.yaml")
fig = wv.plot("simulation.raw", spec)

# Method 2: Dictionary configuration
config = {"title": "Analysis", "x": "time", "y": [{"label": "V", "signals": {"Out": "v(out)"}}]}
fig = wv.plot("simulation.raw", config)
```

#### **Key Features Successfully Implemented**
- **✅ Zero Legacy Code**: Complete removal of SpiceData, reader.py, and all legacy components
- **✅ Single Data Interface**: Only WaveDataset for data loading (no more dual APIs)
- **✅ Modern CLI**: CLI updated to use v1.0.0 API with WaveDataset and plotting functions
- **✅ Clean Package Structure**: Removed all legacy imports and exports
- **✅ Automatic Renderer Detection**: Jupyter vs. standalone execution
- **✅ Clean Import Structure**: Single `import wave_view as wv` line
- **✅ Elegant Namespace**: `wv.PlotSpec`, `wv.plot()`, `wv.load_spice_raw()`, `wv.WaveDataset`
- **✅ Unified API**: One plot() function for all plotting needs
- **✅ Modern Configuration**: Pure PlotSpec with Pydantic validation

## Next Sprint - v1.0.0 Release and Documentation

### 📋 **Test Suite Refactoring** (HIGH PRIORITY)

#### **Legacy Test Cleanup** 
- [X] **Update API Tests**
  - Fix `tests/unit_tests/api/test_load_spice.py` to remove SpiceData references
  - Update tests to use `load_spice_raw()` instead of legacy `load_spice()` 
  - Ensure all API tests pass with WaveDataset-based implementation
  
- [X] **Update Integration Tests**
  - Refactor `tests/test_integration_v1_0_0.py` to use new `plot()` API
  - Fix test methods to work with file-path-based plotting
  - Ensure all v1.0.0 tests pass with updated API
  
- [X] **Legacy Test Archive**
  - Review and update/remove tests that reference SpiceData or other removed components
  - Update plotter tests in `tests/unit_tests/plotter/` directory
  - Consider archiving legacy tests vs. updating them

#### **Stage B – Documentation workflows**
[X] Added tests/workflows/ directory with 4 high-level user-story tests:
    - test_path_plot.py
    - test_preload_plot.py
    - test_yaml_spec_plot.py
    - test_cli_plot.py (CLI smoke)
  All new tests pass.

#### **Stage C – Unit Coverage Rebuild** (IN PROGRESS)
- [X] **Plotting helper tests** – Added `tests/unit/plotting/test_plotting_helpers.py` covering:
  - `_calculate_y_axis_domains()` single/multi
  - `_config_zoom()` logic
  - `add_waveform()` axis assignment + kwargs forwarding
- [X] **WaveDataset core tests** – Added error-path tests (`tests/unit/wavedataset/test_wavedataset_error_paths.py`) – 100 % coverage
- [X] **PlotSpec helper tests** – Added `tests/unit/plotspec/test_plotspec_basic.py` – YAML parse, round-trip, error paths
- [X] **Create layout edge-case tests** – Added `tests/unit/plotting/test_create_layout_edge.py` (domains ordering, log-scale, range, grid, range slider)
- [X] **Stage C complete** – Unit coverage rebuilt with 44 tests passing

### 📋 **Release Preparation Tasks** (HIGH PRIORITY)

#### **Documentation Updates** ✅ **COMPLETED**
- [X] **API Documentation** – All Sphinx pages updated for v1.0.0; obsolete pages removed
- [X] **Examples and Demos** – Examples updated, README refreshed with new API; migration content captured in docs
- [X] **CHANGELOG.rst** – Detailed 1.0.0 entry with breaking changes and features

#### **Version Management**
- [ ] **Version Bump**
  - Update version to 1.0.0 in pyproject.toml
  - Update __version__ in __init__.py
  - Prepare for breaking changes release
  
- [ ] **Final Testing**
  - Run complete test suite with v1.0.0 API
  - Test installation and import in clean environment
  - Validate all examples work correctly

### 📋 **Future Development** (MEDIUM PRIORITY)

#### **Enhanced Features** (v1.1.0)
- [X] **Complex Number Handling** ✅ **COMPLETED**
  - ✅ Add smart complex number handling to `add_waveform()` function
  - ✅ Implement automatic real/magnitude conversion for Plotly compatibility
  - ✅ Fix JSON serialization errors for AC analysis complex signals
  - ✅ Preserve complex number workflow for magnitude/phase calculations in processed_data
  
- [ ] **Advanced Signal Processing**
  - Create utility functions for common signal processing operations
  - Add support for frequency domain analysis helpers
  
- [ ] **Performance Optimizations**
  - Optimize large dataset handling
  - Implement lazy loading for very large SPICE files

#### **Multi-Case Support** (v1.2.0)
- [ ] **PVT Corner Analysis**
  - Design API for corner plotting: `wv.plot_corners()`
  - Support for multiple SPICE files comparison
  
- [ ] **Monte Carlo Visualization**
  - Statistical plotting functions
  - Distribution analysis tools
  
- [ ] **Parameter Sweep Plotting**
  - Support for parametric analysis results
  - Advanced multi-dimensional plotting

#### **CLI Enhancements** (Backlog)
- [ ] **Batch Plotting Mode**
  - Command: `wave_view batch-plot *.raw --spec spec.yml --output-dir plots/`
  - *Status*: **Deferred** until batch loader (`wv.load_spice_raw_batch`) design is finalized
- [ ] **Auto-generate Blank Spec**
  - Command: `wave_view scaffold-spec sim.raw > spec.yml`
  - *Status*: Added to backlog for future discussion
- [ ] **Signals Command Improvements**
  - Add `--grep / --regex` filtering, `--json` output, and colour highlighting
  - *Status*: Discussion required before implementation

## Current Branch Status - v1.0.0 READY 🎯

- **Branch**: `test_suite_refactor`
- **Architecture Status**: ✅ **COMPLETE** - All v1.0.0 phases implemented
- **API Status**: ✅ **UNIFIED** - Single plot() function with clean interface
- **Legacy Code**: ✅ **COMPLETELY REMOVED** - Zero legacy components remain
- **Test Status**: Needs refactoring for removed SpiceData components
- **Demo Status**: ✅ **UPDATED** - Uses clean v1.0.0 API
- **CLI Status**: ✅ **UPDATED** - Uses modern v1.0.0 API exclusively

### **Ready for Release**
- **Code Quality**: Excellent with single-responsibility functions
- **Test Coverage**: 96% on plotting functions, 88% on PlotSpec
- **API Design**: Clean, elegant, and production-ready
- **Documentation**: Needs updating for v1.0.0 API changes
- **Package Structure**: Pure v1.0.0 architecture with zero legacy code

### **Recent Accomplishments**
- **Legacy Reader Removal**: Successfully removed reader.py and SpiceData completely
- **CLI Migration**: Updated CLI to use WaveDataset and v1.0.0 plotting functions
- **Import Cleanup**: Removed all SpiceData references from package
- **Test Cleanup**: Removed legacy reader tests and fixed import issues
- **API Purification**: Package now contains only modern v1.0.0 components

## Notes
- **Current State**: v1.0.0 architecture fully implemented with zero legacy code
- **Next Focus**: Test suite refactoring and documentation updates for release
- **Major Achievement**: Complete elimination of all legacy components - pure v1.0.0 architecture
- **Breaking Changes**: Ready for v1.0.0 major version release with clean migration path

### **Stage D – Coverage & CI**
  - [X] **Overall coverage ≥ 85 %** – Added loader tests; project coverage now 86 %
  - [ ] **Add coverage gate to CI** – Update GitHub Actions workflow / pytest ini
  - [X] **CLI tests** – Added `tests/unit/cli/test_cli_basic.py`; cli.py coverage now 81 %, overall 91 %
  - [X] **Legacy integration test removed** – Deleted redundant `tests/test_integration_v1_0_0.py`; suite now 59 tests
  - [ ] **env helper tests** – Bring `utils/env.py` coverage ≥ 90 %

### 📋 **Engineering Notation Enhancement - COMPLETED** ✅ **FREQUENCY DOMAIN IMPROVEMENT**

#### **Automatic SI Prefix Detection** ✅ **COMPLETED**
- [X] **Enhanced frequency domain plotting** ✅ **COMPLETED**
  - Added automatic detection of frequency signals in X-axis configuration
  - Implemented SI engineering notation (1G, 1M, 1k) instead of American notation (1B, 1M, 1K)
  - Fixed Plotly exponentformat to "SI" for signals containing "frequency" in the name
  - Improves readability for AC analysis and frequency response plots
  
- [X] **Comprehensive test coverage** ✅ **COMPLETED**
  - Added tests for frequency signal detection with and without log scale
  - Added tests to ensure non-frequency signals use default formatting
  - All tests passing with 100% coverage of new functionality
  
- [X] **User experience improvement** ✅ **COMPLETED**
  - Automatic activation - no configuration required from users
  - Works with existing YAML specifications and PlotSpec configurations
  - Maintains backward compatibility for all existing plots