# Project Memory

## Project Overview
Wave_view is a Python package for SPICE simulation visualization with a modern, user-friendly API. The project features core modules for data reading (WaveDataset), v1.0.0 plotting functions (plotting.py), and modern PlotSpec configuration management, with comprehensive YAML-based configuration support and advanced features like log scale plotting and automatic renderer detection.

## Current State
**Version 1.0.0 Architecture Implementation - COMPLETED** 🚀 **MAJOR MILESTONE ACHIEVED**

### **Phase 1.6: Legacy Reader Removal COMPLETED** ✅ **BREAKING CHANGE SUCCESS**
- **Achievement**: Complete removal of legacy reader.py and SpiceData class
- **Breaking Change**: SpiceData class completely removed from public API
- **CLI Migration**: Updated CLI to use WaveDataset and v1.0.0 plotting functions
- **Import Cleanup**: Removed SpiceData from __init__.py exports and all imports
- **Test Cleanup**: Removed entire tests/unit_tests/reader/ directory
- **API Unification**: Only WaveDataset remains for data loading (no more dual APIs)
- **File Removal**: Deleted src/wave_view/core/reader.py completely

### **Phase 1.5: Ultimate API Simplification COMPLETED** ✅ **MAXIMUM SIMPLIFICATION ACHIEVED**
- **Achievement**: Complete removal of redundant API functions AND wrapper layers for maximum clarity
- **Function Elimination**: Removed `_categorize_signals()`, `explore_signals()`, `load_spice()`, and redundant `api.plot()` wrapper
- **Core Exposure**: Direct exposure of `core.plotting.plot()` function for maximum simplicity
- **API Streamlining**: Simplified to just 2 functions: `plot()` (from core) and `load_spice_raw()` (from api)
- **Import Cleanup**: Removed all unnecessary imports and dependencies from public API
- **User Experience**: Explicit data flow - users see exactly what happens: `load_spice_raw()` → `PlotSpec` → `plot()`
- **Breaking Change**: 4 functions removed, API reduced to absolute essentials with zero redundancy

### **Phase 1.4: Legacy Config Removal COMPLETED** ✅ **FINAL CLEANUP SUCCESS**
- **Achievement**: Complete removal of legacy config.py system (commit c9cb970)
- **Legacy Elimination**: Archived config.py as config_legacy.py in _archive/ directory
- **API Purification**: Removed PlotConfig class and all related functions from package
- **Function Cleanup**: Removed config_from_file(), config_from_yaml(), validate_config() functions
- **Import Streamlining**: Cleaned package namespace - only PlotSpec remains for configuration
- **Breaking Change**: 160 lines of legacy code removed, PlotConfig completely superseded by PlotSpec

### **Phase 1.3: Final API Migration COMPLETED** ✅ **BREAKING CHANGE SUCCESS**
- **Achievement**: Successfully migrated from legacy plotter.py to pure v1.0.0 API
- **Legacy Removal**: Completely removed `src/wave_view/core/plotter.py` and `SpicePlotter` class
- **API Unification**: Replaced `plot_v1()` with unified `plot()` function using v1.0.0 architecture internally
- **Clean API**: Single `wv.plot()` function with automatic renderer configuration
- **Import Cleanup**: Removed all SpicePlotter imports from `__init__.py` and `api.py`
- **Demo Update**: Updated example to use clean `wv.plot()` API without plot_v1()

### **v1.0.0 Architecture - FULLY IMPLEMENTED** ✅ **ARCHITECTURE COMPLETE**
- **Phase 1.1**: ✅ **PlotSpec Simplification** - Configuration-only class
- **Phase 1.2**: ✅ **Standalone Plotting Functions** - Complete plotting.py module
- **Phase 1.2+**: ✅ **Code Quality Enhancement** - Refactored functions with single responsibility
- **Phase 1.2++**: ✅ **Plotting Excellence** - Optimal zoom and Y-axis ordering
- **Phase 1.3**: ✅ **Final API Migration** - Unified plot() function and legacy removal
- **Phase 1.4**: ✅ **Legacy Config Removal** - Complete elimination of config.py system
- **Phase 1.5**: ✅ **Ultimate API Simplification** - Maximum API reduction with zero redundancy
- **Phase 1.6**: ✅ **Legacy Reader Removal** - Complete SpiceData elimination

### **Current v1.0.0 API - PURE MODERN ARCHITECTURE** 🎯 **ZERO LEGACY CODE**
```python
import wave_view as wv

# Ultra-simple explicit workflow (only way to use the API)
data, metadata = wv.load_spice_raw("simulation.raw")
print(f"Available signals: {list(data.keys())}")  # Direct signal examination

spec = wv.PlotSpec.from_yaml("""
title: "My Analysis"
x:
  signal: "time"
  label: "Time (s)"
  log_scale: false
y:
  - label: "Voltage (V)"
    signals:
      Output: "v(out)"
""")

fig = wv.plot(data, spec)  # Core plotting function - no wrapper!
fig.show()  # Explicit display control
```

### **Key Features Completed**
- **✅ Zero Legacy Code**: Complete removal of SpiceData, reader.py, and all legacy components
- **✅ Single Data Interface**: Only WaveDataset for data loading (no more dual APIs)
- **✅ Modern CLI**: CLI updated to use v1.0.0 API with WaveDataset and plotting functions
- **✅ Clean Package Structure**: Removed all legacy imports and exports
- **✅ Automatic Renderer Detection**: Jupyter vs. standalone execution
- **✅ Clean Import Structure**: Single `import wave_view as wv`
- **✅ Ultra-Minimalist Namespace**: **ONLY** `wv.PlotSpec`, `wv.plot()`, `wv.load_spice_raw()`, `wv.WaveDataset` 
- **✅ Direct Core Exposure**: `plot()` function is the actual core function, no wrapper layers
- **✅ Modern Configuration**: Pure PlotSpec with Pydantic validation and XAxisSpec support
- **✅ Explicit Data Flow**: Users see exactly what happens: load → configure → plot → show
- **✅ Zero Redundancy**: No duplicate functions, no wrappers, no hidden complexity
- **✅ Complex Number Handling**: Automatic conversion of AC analysis complex signals for Plotly compatibility
- **✅ X-Axis Configuration**: Full XAxisSpec support with labels, log scale, and range limits

### **Previous Milestones**
- **Phase 1.6: Legacy Reader Removal** - Complete elimination of SpiceData class and reader.py
- **Phase 1.5: Ultimate API Simplification** - Maximum API reduction with zero redundancy
- **Phase 1.4: Legacy Config Removal** - Complete elimination of config.py system
- **Phase 1.3: Final API Migration** - Unified plot() function and legacy removal
- **Phase 1.2++: Plotting Excellence** - Significantly improved plotting usability
- **Phase 1.2+: Code Quality Enhancement** - 75% complexity reduction with function extraction
- **Phase 1.2: Standalone Plotting Functions** - Complete v1.0.0 plotting module
- **Phase 1.1: PlotSpec Simplification** - Configuration-only class achieved

### **TDD Methodology Success** ✅ **DEVELOPMENT APPROACH VALIDATION**
- **Comprehensive Testing**: 10 tests passing for plotting functions
- **High Coverage**: plotting.py 96% coverage, PlotSpec 88% coverage
- **Clean Code**: Single-responsibility functions with clear separation of concerns
- **Incremental Development**: Red → Green → Refactor cycle throughout

## Key Decisions

### **Version 1.0.0 Final Architecture**
- **Single Data Interface**: WaveDataset as the only data loading mechanism
- **Complete Legacy Removal**: No more SpiceData class or reader.py module
- **Unified API**: Single `wv.plot()` function with clean interface
- **Modern CLI**: CLI uses v1.0.0 API exclusively
- **Function-Based Design**: Clean separation between configuration (PlotSpec) and plotting (plotting.py)
- **Automatic Setup**: Renderer configuration happens on package import
- **Direct Signal Lookup**: Simple Dict[str, np.ndarray] interface without complex resolution

### **Breaking Changes Successfully Implemented**
- **Data Loading**: `wv.load_spice_raw()` returns Dict[str, np.ndarray] format
- **API Simplification**: `wv.plot(data, spec)` replaces all legacy plotting methods
- **Import Cleanup**: SpiceData completely removed from public API
- **Configuration Format**: PlotSpec format as the standard (PlotConfig completely removed)
- **Data Interface**: Dict[str, np.ndarray] as the uniform data format
- **Class Removal**: SpiceData class no longer exists in the package
- **Function Removal**: All legacy functions removed from public API

### **Architecture Principles Applied**
- **Single Responsibility**: Each function has one clear purpose
- **Separation of Concerns**: Configuration vs. visualization cleanly separated
- **User Experience**: Automatic renderer detection and clean imports
- **Extensibility**: Architecture designed for future multi-case plotting support
- **Modern Design**: Only WaveDataset for data loading with metadata support

## Current API (v1.0.0) - FINAL
```python
# Clean v1.0.0 API Pattern – single explicit workflow
import wave_view as wv

# 1. Load data
data, metadata = wv.load_spice_raw("simulation.raw")

# 2. Create PlotSpec (YAML string / file / dict)
spec = wv.PlotSpec.from_yaml("""
title: "My Analysis"
x:
  signal: "time"
  label: "Time (s)"
y:
  - label: "Voltage (V)"
    signals: {Out: "v(out)"}
""")

# 3. Plot using the pre-loaded dictionary
fig = wv.plot(data, spec)
fig.show()
```

## Release Status
- **Current Version**: 1.0.1 (Published to PyPI) ✅ **SUCCESSFUL HOTFIX RELEASE**
- **Previous Versions**: 0.1.0, 1.0.0 (Published to PyPI)
- **Migration Status**: ✅ **COMPLETE** - v1.0.1 verified working in fresh environment
- **API Stability**: Production-ready with clean, unified interface
- **Legacy Code**: ✅ **COMPLETELY ELIMINATED** - Zero legacy components remain
- **Critical Fix**: v1.0.1 adds missing pydantic dependency (v1.0.0 had import error)

## Architecture Status
- **Clean 3-Step Workflow**: Discovery → Configuration → Plotting
- **Package Quality**: Production-ready with comprehensive feature set
- **Test Coverage**: 96% on plotting functions, 88% on PlotSpec
- **Code Quality**: Excellent - clean functions with single responsibilities
- **Documentation**: Complete Sphinx documentation system (needs update for v1.0.0)
- **Legacy Code**: ✅ **COMPLETELY REMOVED** - No more reader.py, plotter.py, SpicePlotter, SpiceData, or config.py dependencies

## Recent Achievements (Latest Session)

### **CLI Enhancement - Self-Contained YAML Specifications** ✅ **COMPLETED**
- **Optional raw: field**: Added to PlotSpec class for self-contained YAML specifications
- **Flexible CLI usage**: 3 ways to specify raw file with clear precedence order:
  1. `--raw` option (highest priority)
  2. Positional argument: `waveview plot spec.yaml sim.raw`
  3. `raw:` field in YAML specification (lowest priority)
- **Smart warning system**: CLI overrides emit helpful warnings when conflicting with YAML
- **Comprehensive error handling**: Clear error messages when no raw file is specified
- **Updated CLI help**: Complete documentation of new usage patterns
- **5 new CLI tests**: Comprehensive coverage of all raw file specification scenarios

### **Scale Syntax Enhancement** ✅ **COMPLETED**
- **Intuitive syntax support**: Both `scale: "log"` and legacy `log_scale: true` now supported
- **Backward compatibility**: All existing YAML files continue to work unchanged
- **Consistent implementation**: Works for both X and Y axes with same syntax
- **3 new tests**: Complete coverage of scale syntax combinations and PlotSpec integration
- **Root cause resolution**: Fixed original log scale configuration issue

### **Quality Improvements**
- **Test coverage expansion**: Added 8 new tests (5 CLI + 3 scale syntax)
- **CLI test suite**: Now 12 comprehensive tests covering all CLI functionality
- **Zero regressions**: All existing functionality maintained
- **Production ready**: Enhanced CLI with professional user experience

## Open Questions
- **CLI Refinement**: Continue CLI enhancements (batch processing, signal filtering, spec scaffolding)
- **Test Suite Refactoring**: Complete remaining legacy test cleanup
- **Documentation Updates**: Update all examples and documentation for v1.0.0
- **Migration Guide**: Create guide for users upgrading from v0.x.x to v1.0.0

## Development Branch Status (2025-07-06)
- New branch `test_suite_refactor` created from `1.0.0` to host the aggressive test-suite refactor aligned with v1.0.0 API.
- `1.0.0` branch pushed to origin and now serves as stable baseline.

- **Test Suite Refactor – Stage C (Unit Coverage) IN PROGRESS**:
  * Plotting helper tests added (`tests/unit/plotting/test_plotting_helpers.py`) – `core.plotting` ≥90 %
  * WaveDataset error-path tests added (`tests/unit/wavedataset/test_wavedataset_error_paths.py`) – `core.wavedataset` 100 % coverage
  * PlotSpec helper tests added (`tests/unit/plotspec/test_plotspec_basic.py`) – covers YAML parsing, dict export, and error handling
  * Layout edge-case tests added (`tests/unit/plotting/test_create_layout_edge.py`) – Stage C unit coverage rebuild complete (44 tests passing)
  * Loader tests added (`tests/unit/loader/test_loader_basic.py`) – project coverage now 86 %, Stage D coverage target met
  * CLI tests added (`tests/unit/cli/test_cli_basic.py`) – overall coverage at 91 %, cli.py 81 %
  * Removed outdated integration test (`tests/test_integration_v1_0_0.py`) – suite count 59 tests, no coverage impact

## Recent Documentation Work (2025-07-06)
- Full Sphinx documentation **fully aligned** with final v1.0.0 API.
  * Removed all direct `wv.plot("file.raw", ...)` examples – now always load data first.
  * Eliminated `processed_data` parameter; examples append derived signals to the data dict.
  * Lower-case `x:` / `y:` keys and current option names (`height`, `zoom_buttons`, …) used everywhere.
  * Quickstart, Configuration, Examples, and Index pages updated; build is warning-free.
  * **Documentation Compilation COMPLETED** (2025-07-11): Sphinx docs successfully recompiled with all v1.0.0 changes
  * Remaining tasks: bump package/version strings to 1.0.0.
