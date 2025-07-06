# Project Memory

## Project Overview
Wave_view is a Python package for SPICE simulation visualization with a modern, user-friendly API. The project features core modules for configuration management (config.py), data reading (reader.py), and plotting (plotter.py), with comprehensive YAML-based configuration support and advanced features like log scale plotting and processed signal generation.

## Current State
**Version 1.0.0 Architecture Implementation - Phase 1.2 COMPLETED** 🚀 **TDD SUCCESS**

### **Phase 1.2: Standalone Plotting Functions COMPLETED** ✅ **MAJOR MILESTONE**
- **Achievement**: Successfully implemented v1.0.0 standalone plotting functions using strict TDD methodology
- **New Module**: Created `src/wave_view/core/plotting.py` with clean function-based API
- **Core Functions**: 
  - `plot(data: Dict[str, np.ndarray], spec: PlotSpec)` - Main plotting function
  - `create_figure()` - Empty figure creation
  - `create_layout()` - Layout configuration
  - `add_waveform()` - Trace addition helper
- **API Integration**: Exported as `wave_view.plot_v1()` for testing and transition
- **Direct Signal Lookup**: No complex resolution logic, simple dictionary access
- **Multi-Axis Support**: Full support for multiple Y-axes with proper domain calculation

### **TDD Methodology Success - Phase 1.2** ✅ **DEVELOPMENT APPROACH VALIDATION**
- **Red Phase**: Created 7 failing tests for plotting functions ✅
- **Green Phase**: Implemented functions to make all tests pass ✅
- **Integration**: Added real data integration tests ✅
- **Results**: 15 tests passing (100% pass rate)
- **Coverage**: plotting.py 93% coverage, PlotSpec 88% coverage
- **Quality**: Clean separation of concerns, no coupling to old architecture

### **v1.0.0 Implementation Progress**
- **Phase 1.1**: ✅ **PlotSpec Simplification** - COMPLETED
  - ✅ Removed plotting methods from PlotSpec class
  - ✅ Focus on configuration-only functionality
  - ✅ Maintained factory methods (`from_yaml`, `from_file`)
  - ✅ Added clean `to_dict()` export method
- **Phase 1.2**: ✅ **Standalone Plotting Functions** - COMPLETED
  - ✅ Created `plotting.py` module with function-based API
  - ✅ Implemented `plot()`, `create_figure()`, `create_layout()`, `add_waveform()`
  - ✅ Direct signal lookup without complex resolution
  - ✅ Multi-axis support with proper domain calculation
  - ✅ Full test coverage with real data integration tests
- **Phase 1.3**: 🔄 **Next** - API Migration and Final Cleanup

### **Current Branch**: `1.0.0` 
- **Working Directory**: Ready for commit
- **Test Status**: All v1.0.0 tests passing (15/15)
- **Coverage**: plotting.py 93%, PlotSpec 88%
- **Files Added**: 
  - `src/wave_view/core/plotting.py` - New v1.0.0 plotting functions
  - `tests/unit_tests/test_plotting_v1_0_0.py` - Comprehensive unit tests
  - `tests/test_integration_v1_0_0.py` - Integration tests with real data
- **Files Modified**: 
  - `src/wave_view/__init__.py` - Added plot_v1 export

### **Phase 1.2 Implementation Details**
- **Architecture Compliance**: Perfect adherence to v1.0.0 architecture design
- **Simple Data Interface**: `Dict[str, np.ndarray]` input, no complex objects
- **PlotSpec Integration**: Clean use of `spec.to_dict()` for configuration
- **Multi-Axis Excellence**: Proper domain calculation and Y-axis assignment
- **Error Handling**: Clear error messages for missing signals
- **Theme Support**: Full Plotly theme integration
- **Real Data Validation**: Integration tests with actual Ring Oscillator SPICE data

### **PlotSpec v1.0.0 Refactoring COMPLETED** ✅ **MAJOR MILESTONE**
- **Achievement**: Successfully refactored PlotSpec from v0.2.0 to v1.0.0 architecture using strict TDD methodology
- **Configuration-Only Class**: PlotSpec now focuses purely on configuration validation and export
- **Breaking Changes**: Removed plotting methods (`plot()`, `show()`, `get_figure()`, `_to_legacy_config()`)
- **New Functionality**: Added clean `to_dict()` method for v1.0.0 plotting functions
- **Archive Created**: v0.2.0 implementation preserved in `src/wave_view/_archive/plotspec_v0_2_0.py`

### **Major Architecture Decision: v1.0.0 API Simplification** 
- **Architecture Document**: Complete v1.0.0 architecture design documented in `context/architecture_v1.0.0.md`
- **Breaking Changes**: Major API simplification with function-based approach
- **Future Extensibility**: Designed for multi-case plotting (PVT, Monte Carlo, parameter sweeps)
- **Implementation Plan**: Phase 1.1 and 1.2 completed successfully ✅

## Key Decisions

### **Version 1.0.0 Architecture (Major Refactoring)**
- **Function-Based API**: Shift from `spec.plot(data)` to `wv.plot_v1(data, spec)` for better extensibility
- **Separation of Concerns**: PlotSpec handles only configuration, plotting functions handle only visualization
- **Direct Signal Lookup**: Replace complex resolution with simple `Dict[str, np.ndarray]` access
- **Multi-Case Foundation**: Architecture designed for future multi-case plotting support

### **TDD-Driven Development**
- **Methodology**: Strict Red → Green → Refactor cycle with immediate test verification
- **Quality Results**: 93% plotting function coverage, 88% PlotSpec coverage
- **Success Metrics**: 15/15 tests passing with comprehensive integration tests
- **Architecture Validation**: Clean separation of concerns achieved without coupling

### **Breaking Changes for v1.0.0**
- **PlotSpec Methods Removed**: `plot()`, `show()`, `get_figure()` methods removed
- **New API**: `wave_view.plot_v1(data: Dict[str, np.ndarray], spec: PlotSpec)`
- **Signal Interface**: Direct dictionary lookup instead of complex resolution
- **Migration Strategy**: Gradual transition with `plot_v1` during development

## Current API (v1.0.0)
```python
# New v1.0.0 API Pattern
import wave_view as wv

# Load data and convert to simple format
spice_data = wv.load_spice("simulation.raw")
data = {signal: spice_data.get_signal(signal) for signal in spice_data.signals}

# Create configuration
spec = wv.PlotSpec.from_yaml("""
title: "SPICE Analysis"
x: "time"
y:
  - label: "Voltage (V)"
    signals:
      Output: "v(out)"
""")

# Plot with v1.0.0 function
fig = wv.plot_v1(data, spec)
fig.show()
```

## Release Status
- **Current Version**: 0.1.0 (Published to PyPI)
- **Next Version**: 1.0.0 (Breaking changes with v1.0.0 architecture)
- **PyPI Status**: ✅ **LIVE** - https://pypi.org/project/wave-view/
- **Installation**: `pip install wave_view` (v0.1.0)

## Architecture Status
- **Clean 3-Step Workflow**: Discovery → Configuration → Plotting
- **Package Quality**: Production-ready with comprehensive feature set
- **Test Coverage**: 93% on new plotting functions, 88% on PlotSpec
- **Documentation**: Complete Sphinx documentation system
