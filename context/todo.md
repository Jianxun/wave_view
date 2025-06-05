# Project Todo List

## Current Sprint - Core Waveform Visualization
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

## Sprint 2 - Signal Discovery & Exploration
- [ ] Integrate `SpiceSignalExplorer` class into core package
- [ ] Add signal categorization and metadata extraction 
- [ ] Implement `SpiceExplorer` API (`wv.SpiceExplorer()`)
- [ ] Create signal discovery convenience functions (`wv.explore_signals()`, `wv.suggest_config()`)
- [ ] Add Jupyter integration with rich HTML displays
- [ ] Implement interactive signal selector widgets
- [ ] Add configuration validation and suggestions
- [ ] Create signal search and filtering capabilities

## Sprint 3 - Advanced Features
- [ ] Add signal processing utilities (core/processor.py)
- [ ] Create YAML template generators (utils/templates.py)
- [ ] Add export functionality (HTML, PNG, PDF)
- [ ] Create example configurations (examples/configs/)
- [ ] Build example Jupyter notebooks (examples/notebooks/)
- [ ] Implement batch plotting functionality (`plot_batch`, `plot_multi`)

## Future Backlog
- [ ] Interactive widget integration with ipywidgets
- [ ] Quick plot with auto-detection (`quick_plot`)
- [ ] Configuration builder class (`ConfigBuilder`)
- [ ] Performance optimization for large datasets
- [ ] Advanced signal processing functions (FFT, filtering, etc.)
- [ ] Custom measurement tools (cursors, calculations)
- [ ] Package for PyPI distribution
- [ ] Comprehensive documentation and tutorials

## Completed Tasks
- [X] Initialize project directory structure
- [X] Create context management system
- [X] Set up project structure with virtual environment and requirements.txt
- [X] Create experimental notebook for testing plotly widgets
- [X] **Research SPICE file formats and parsing libraries** (spicelib confirmed)
- [X] **Create working prototype** (prototype/script/plot.py)
- [X] **Test prototype with real SPICE data** (Ring_Oscillator_7stage.raw)
- [X] **Fix browser rendering issues** (Plotly configuration)
- [X] **Design package architecture** (core classes and API)
- [X] **Create implementation plan** (doc/implementation_plan.md)
- [X] **Analyze configuration file strategies** (single vs multi-figure)
- [X] **Prototype signal discovery API** (signal_explorer.py, jupyter_signal_browser.py)
- [X] **Document signal discovery features** (doc/signal_discovery_api.md)

## Implementation Notes
- **Focus**: Core visualization first, then discovery features
- Prototype proved the technical approach works well
- spicelib + Plotly + YAML configuration is a solid foundation
- Multi-figure YAML format is clean and intuitive
- Browser integration works properly with `pio.renderers.default = "browser"`
- Signal discovery prototypes ready for integration in Sprint 2
- Ready to begin systematic implementation of the main package 