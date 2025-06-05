# Project Memory

## Project Overview
Wave View - A Python package for visualizing SPICE simulation waveforms, designed primarily for Jupyter notebook integration. The package provides both simple plotting functions and advanced signal processing capabilities through a clean, intuitive API.

## Current State
- **Sprint 1 Complete**: ✅ Core waveform visualization package implemented and tested
- **Package Structure**: Full `wave_view/` package with core modules and API
- **Real Data Testing**: All functionality verified with Ring_Oscillator_7stage.raw file
- **Case Normalization**: All signal names normalized to lowercase for user consistency
- **Ready for Sprint 2**: Signal discovery and exploration features

## Key Decisions
- **Plotly chosen** as the visualization backend for interactive plotting and browser integration
- **Dual API approach**: Simple `wv.plot()` for basic use, advanced `SpicePlotter` class for power users
- **YAML-based configuration** with support for both single and multi-figure configs
- **Jupyter-first design** with auto-display and interactive features
- **spicelib library** confirmed working for .raw file reading
- **Flexible signal processing** with support for both raw signals (`raw.signal`) and processed signals (`data.signal`)
- **Case-insensitive signal access**: All signal names normalized to lowercase (e.g., `V(VDD)` → `v(vdd)`)

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

## Technical Stack Confirmed
- **Core**: Python 3.8+, NumPy, spicelib, PyYAML
- **Visualization**: Plotly (with browser integration)
- **Configuration**: YAML files with validation
- **Target Environment**: Jupyter notebooks, but also standalone Python scripts
- **Signal Access**: Case-insensitive, normalized to lowercase 