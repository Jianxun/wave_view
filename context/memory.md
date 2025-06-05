# Project Memory

## Project Overview
Wave View - A Python package for visualizing SPICE simulation waveforms, designed primarily for Jupyter notebook integration. The package provides both simple plotting functions and advanced signal processing capabilities through a clean, intuitive API.

## Current State
- **Prototype Complete**: Working SPICE waveform plotting script with Plotly integration
- **Architecture Designed**: Comprehensive implementation plan created with API design
- **Multi-configuration Support**: Supports both single-figure and multi-figure YAML configurations
- **Ready for Implementation**: All core design decisions made, ready to build the main package

## Key Decisions
- **Plotly chosen** as the visualization backend for interactive plotting and browser integration
- **Dual API approach**: Simple `wv.plot()` for basic use, advanced `SpicePlotter` class for power users
- **YAML-based configuration** with support for both single and multi-figure configs
- **Jupyter-first design** with auto-display and interactive features
- **spicelib library** confirmed working for .raw file reading
- **Flexible signal processing** with support for both raw signals (`raw.signal`) and processed signals (`data.signal`)

## Open Questions
- Signal processing function library - which common calculations to include?
- Export format priorities (HTML, PNG, PDF, SVG)?
- Interactive widget integration level (basic vs advanced controls)?
- Performance optimization strategies for very large datasets?

## Recent Progress
- Created working prototype in `prototype/script/plot.py` with full Plotly integration
- Fixed browser rendering issues (was printing HTML to terminal)
- Tested with Ring_Oscillator_7stage.raw file successfully
- Designed comprehensive package architecture with core classes:
  - `SpiceData` for file reading and signal access  
  - `PlotConfig` for configuration management
  - `SpicePlotter` for advanced plotting workflows
- Created detailed implementation plan saved to `doc/implementation_plan.md`
- Analyzed multi-figure configuration approach vs separate config files

## Technical Stack Confirmed
- **Core**: Python 3.8+, NumPy, spicelib, PyYAML
- **Visualization**: Plotly (with browser integration)
- **Configuration**: YAML files with validation
- **Target Environment**: Jupyter notebooks, but also standalone Python scripts 