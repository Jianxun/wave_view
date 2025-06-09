# Project Todo List

## Current Sprint

### 🧪 Test Suite Development (High Priority)
Based on development guidelines, comprehensive test-driven development needed for new features:

- [X] **Core Config Tests Complete**: Comprehensive unit tests for PlotConfig class (33 tests, 96% coverage) ✅
  - All initialization methods (dict, list, YAML file/string, Path objects)
  - File vs content detection logic
  - Configuration validation with error checking
  - Multi-figure support, templates, raw file path resolution
  - **NEW**: Log scale support testing
  - **NEW**: Processed signal validation testing
- [X] **Core Plotter Tests Complete**: Comprehensive modular unit tests for SpicePlotter class (47 tests, 93% coverage) ✅
  - **test_plotter_basic.py**: Initialization, method chaining, properties, string representation (18 tests)
  - **test_plotter_processed.py**: Processed signals functionality, error handling, integration (16 tests)
  - **test_plotter_log_scale.py**: Log scale support for X/Y axes, edge cases, data integrity (13 tests)
  - **Shared utilities**: Mock data, test configs, assertion helpers in `__init__.py`
  - **Modular structure**: Easy to maintain, focused test files for different functionality areas
- [ ] **Core Reader Tests**: Unit tests for SpiceData class
- [ ] **API Integration Tests**: Test new processed_data parameter and log scale API
- [ ] **Demo Script Validation**: Ensure all demo scripts work as integration tests
- [ ] **Update existing integration tests** for new features
- [ ] **Edge case testing** - invalid scale values, missing processed signals, etc.

## Recently Completed ✅

### 🚀 Major API Enhancements (This Session)
- [X] **Processed Data API Enhancement**: Modified plot() function to accept processed_data parameter
- [X] **Clean User Interface**: Eliminated need for users to access internal SpicePlotter class
- [X] **YAML Integration**: Processed signals referenced with "data." prefix in configurations
- [X] **Log Scale Support**: Added logarithmic axis scaling for both X and Y axes
- [X] **Bode Plot Support**: Perfect for frequency response plots with log frequency axis
- [X] **Comprehensive Examples**: Created demo_log_scale.py and updated demo_ota_5t.py
- [X] **Validation Testing**: Verified log scales properly applied to Plotly figures

### 📦 Repository & Package Foundation  
- [X] Repository reorganization for PyPI publication
- [X] Implement src/ layout structure  
- [X] Consolidate tests directory
- [X] Move examples and demo files to examples/
- [X] Create modern Python packaging (pyproject.toml)
- [X] Add MIT LICENSE for open source
- [X] Add development requirements (requirements-dev.txt)
- [X] Fix broken imports after reorganization
- [X] Package installable via pip install -e . ✅
- [X] Validate core API functionality
- [X] Fix demo script import issue (context recovery session)
- [X] Fix x-axis positioning to appear at bottom of figure (with range slider preserved)
- [X] Fix Y-axis domain calculation (removed incorrect reverse() call)
- [X] Fix Y-axis order UX - first in config now appears at top of plot (intuitive reading order)
- [X] Update README.md with comprehensive installation instructions (dev mode + GitHub)

## Backlog - Sprint 2 & Beyond

### Documentation & Publication
- [ ] Polish README.md for PyPI
- [ ] Create comprehensive documentation (Sphinx)
- [ ] Add usage examples to docs/examples/
- [ ] Set up GitHub Actions for CI/CD
- [ ] Publish to PyPI (python -m build, twine upload)

### Signal Exploration UI (Sprint 2)
- [ ] Implement SpiceSignalExplorer class
- [ ] Add Jupyter widget for signal browsing
- [ ] Create interactive signal selection interface
- [ ] Integrate with existing plotting system

### Advanced Features (Future)
- [ ] Export functionality (PNG, PDF, SVG)
- [ ] Performance optimization for large datasets
- [ ] Additional signal processing functions
- [ ] Advanced annotation and markup tools
- [ ] Multi-simulation comparison features

### Code Quality
- [ ] Fix pytest return warnings (cosmetic only)
- [ ] Add type hints throughout codebase
- [ ] Improve test coverage to 100%
- [ ] Add pre-commit hooks for code quality

## Completed Tasks - Sprint 1

### Core Package Implementation ✅
- [X] Design package structure and API
- [X] Implement SpiceData class with case-insensitive access
- [X] Implement PlotConfig class with YAML support
- [X] Implement SpicePlotter class with advanced features
- [X] Create main API functions (plot, load_spice, etc.)
- [X] Add processed signal generation capability
- [X] Implement multi-figure plotting support

### Testing & Validation ✅  
- [X] Write comprehensive unit tests
- [X] Write integration tests
- [X] Test with real SPICE data
- [X] Validate YAML configuration system
- [X] Test Jupyter notebook integration
- [X] Verify case-insensitive signal access

### User Experience ✅
- [X] Implement auto-configuration generation
- [X] Add template creation functionality
- [X] Support multiple config formats (file, dict, string)
- [X] Auto-detect Jupyter vs standalone environments
- [X] Add manual renderer control
- [X] Create helpful error messages and validation

### Project Setup ✅
- [X] Set up development environment
- [X] Configure testing framework
- [X] Establish code organization patterns
- [X] Document API design decisions
- [X] Create example usage scenarios

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