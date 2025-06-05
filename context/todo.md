# Project Todo List

## Current Sprint - Package Polishing & User Experience
- [ ] Enhanced plotting aesthetics and themes
- [ ] Interactive widgets and controls (zoom, pan, measurements)
- [ ] Signal processing function library (FFT, filtering, etc.)
- [ ] Export functionality (HTML, PNG, PDF, SVG)
- [ ] Performance optimization for large datasets
- [ ] Enhanced error messages and user guidance
- [ ] Documentation and examples
- [ ] Packaging for PyPI distribution

## Sprint 2 - Signal Discovery & Exploration
- [ ] Integrate `SpiceSignalExplorer` class into core package
- [ ] Add signal categorization and metadata extraction 
- [ ] Implement `SpiceExplorer` API (`wv.SpiceExplorer()`)
- [ ] Create signal discovery convenience functions (`wv.explore_signals()`, `wv.suggest_config()`)
- [ ] Add Jupyter integration with rich HTML displays
- [ ] Implement interactive signal selector widgets
- [ ] Add configuration validation and suggestions
- [ ] Create signal search and filtering capabilities

## Future Backlog
- [ ] Quick plot with auto-detection (`quick_plot`)
- [ ] Configuration builder class (`ConfigBuilder`)
- [ ] Custom measurement tools (cursors, calculations)
- [ ] Multi-file comparison and overlay plotting
- [ ] Statistical analysis functions
- [ ] Comprehensive documentation and tutorials

## Completed Tasks - Sprint 1: Core Functionality
- [X] Create main package structure (`wave_view/`)
- [X] Implement `SpiceData` class (core/reader.py) - basic SPICE file reading with case-insensitive access
- [X] Implement `PlotConfig` class (core/config.py) - YAML configuration handling with multi-figure support
- [X] Port plotting logic to `SpicePlotter` class (core/plotter.py)
- [X] Create main API functions in `__init__.py` (`plot()`, `load_spice()`)
- [X] Add multi-figure configuration support
- [X] Create basic unit tests for core functionality
- [X] Test package installation and imports
- [X] Add case-insensitive signal name normalization (all lowercase)
- [X] Create integration tests with real SPICE data
- [X] **Jupyter Integration**: Environment detection and inline plotting
- [X] **Manual renderer control**: `wv.set_renderer()` function
- [X] **YAML string support**: Direct multi-line YAML configurations
- [X] **Template generation**: Auto-create configs from SPICE files
- [X] **Configuration validation**: Real-time validation with helpful warnings

## Implementation Notes
- **Sprint 1 Complete**: ✅ All core functionality implemented and tested
- **User Experience**: Package is very user-friendly with multiple config formats
- **Jupyter-first**: Auto-detects notebooks and provides inline plotting
- **YAML flexibility**: Files, strings, or dictionaries all supported
- **Case handling**: All signal names normalized to lowercase for consistency
- **Next Focus**: Polish the plotting experience, themes, and advanced features
- **Ready for users**: Package provides excellent foundational experience 