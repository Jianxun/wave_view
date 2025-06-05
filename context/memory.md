# Project Memory

## Project Overview
Wave View - A Python package for visualizing SPICE simulation waveforms, designed primarily for Jupyter notebook integration. The package provides both simple plotting functions and advanced signal processing capabilities through a clean, intuitive API.

## Current State
- **Sprint 1 Complete**: ✅ Core waveform visualization package implemented and tested
- **Package Structure**: Full `wave_view/` package with core modules and API
- **Real Data Testing**: All functionality verified with Ring_Oscillator_7stage.raw file
- **Case Normalization**: All signal names normalized to lowercase for user consistency
- **Jupyter Integration**: ✅ Auto-detection and inline plotting support
- **YAML String Support**: ✅ Direct YAML string configurations (no files needed)
- **Ready for Polishing**: Core functionality complete, ready for UI/UX improvements

## Key Decisions
- **Plotly chosen** as the visualization backend for interactive plotting and browser integration
- **Dual API approach**: Simple `wv.plot()` for basic use, advanced `SpicePlotter` class for power users
- **YAML-based configuration** with support for both single and multi-figure configs
- **Jupyter-first design** with auto-display and interactive features
- **spicelib library** confirmed working for .raw file reading
- **Flexible signal processing** with support for both raw signals (`raw.signal`) and processed signals (`data.signal`)
- **Case-insensitive signal access**: All signal names normalized to lowercase (e.g., `V(VDD)` → `v(vdd)`)
- **Environment-aware rendering**: Auto-detects Jupyter vs standalone for appropriate display
- **YAML string support**: Can use inline YAML strings instead of separate config files

## Open Questions
- Signal processing function library - which common calculations to include?
- Export format priorities (HTML, PNG, PDF, SVG)?
- Interactive widget integration level (basic vs advanced controls)?
- Performance optimization strategies for very large datasets?

## Recent Progress
- ✅ **Implemented complete Wave View package**:
  - `SpiceData` class with case-insensitive signal access
  - `PlotConfig` class with multi-figure support and validation
  - `SpicePlotter` class with fluent API and processed signals
  - Main API functions (`plot()`, `load_spice()`, etc.)
- ✅ **All unit tests passing** (12/12)
- ✅ **All integration tests passing** (6/6)
- ✅ **Real SPICE data verification** with Ring Oscillator test case
- ✅ **Case normalization implemented** - all signals accessible as lowercase
- ✅ **Auto-configuration working** - can plot without config files
- ✅ **Template generation working** - creates proper YAML configs
- ✅ **Jupyter integration implemented** - auto-detects environment for inline plots
- ✅ **Manual renderer control** - `wv.set_renderer()` for user control
- ✅ **YAML string support** - use multi-line strings directly as configurations

## User Experience Features
- **Simple API**: `wv.plot(file)` for instant visualization
- **Case-insensitive signals**: `V(VDD)`, `v(vdd)`, `V(vdd)` all work
- **Multiple config formats**: Files, dictionaries, or YAML strings
- **Environment detection**: Works in Jupyter notebooks and standalone scripts
- **Manual overrides**: Full user control when auto-detection fails
- **Comprehensive validation**: Helpful error messages and warnings
- **Template generation**: Auto-creates configs from SPICE files

## Technical Stack Confirmed
- **Core**: Python 3.8+, NumPy, spicelib, PyYAML
- **Visualization**: Plotly (with browser integration)
- **Configuration**: YAML files, strings, or dictionaries with validation
- **Target Environment**: Jupyter notebooks (primary), but also standalone Python scripts
- **Signal Access**: Case-insensitive, normalized to lowercase
- **Rendering**: Environment-aware (inline for notebooks, browser for scripts) 