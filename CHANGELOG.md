# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-07-19

### Added
- **Enhanced CLI Documentation**
  - Dedicated CLI reference page with automatic generation from Click commands
  - Complete command-line interface documentation using `sphinx-click`
  - Comprehensive examples for all CLI commands and options

- **Improved Documentation Structure**
  - Dedicated schema reference page with automatic Pydantic model documentation
  - Restructured quickstart guide with two distinct workflows:
    - **Option A: CLI-First** - Fast workflow for quick visualizations
    - **Option B: Python API** - Flexible workflow for scripting and notebooks
  - Enhanced configuration guide with better organization and examples
  - Cross-references between documentation sections for better navigation

- **Schema Documentation**
  - Automatic generation of PlotSpec schema documentation from Pydantic models
  - Complete field-by-field reference for `PlotSpec`, `XAxisSpec`, and `YAxisSpec`
  - Always up-to-date schema documentation that reflects code changes
  - Professional formatting with type information and validation rules

### Improved
- **CLI User Experience**
  - Clear separation between CLI and API workflows in documentation
  - Better examples showing CLI command usage patterns
  - Improved help text and command descriptions
  - Enhanced workflow guidance for different use cases

- **Documentation Quality**
  - Better organization with dedicated pages for different topics
  - Improved cross-referencing between related sections
  - More comprehensive examples and use cases
  - Professional formatting and consistency

### Technical
- **Documentation Infrastructure**
  - Added `autodoc_pydantic` extension for automatic schema generation
  - Enhanced Sphinx configuration for better documentation building
  - Improved development dependencies for documentation tooling

## [1.0.1] - 2025-07-11

### Fixed
- Minor bug fixes and improvements

## [1.0.0] - 2025-07-11

### Added
- **Modern API Architecture**
  - Complete v1.0.0 API redesign with ultra-minimalist namespace
  - `PlotSpec` class for modern configuration management with Pydantic validation
  - `WaveDataset` for structured data loading with metadata support
  - `plot()` function for unified plotting (replaced legacy SpicePlotter)
  - `load_spice_raw()` for direct SPICE data loading as Dict[str, np.ndarray]
  - Automatic renderer detection for Jupyter vs. standalone execution

- **Command Line Interface**
  - Updated CLI to use v1.0.0 API exclusively
  - Both `plot` and `signals` commands use modern WaveDataset interface
  - Clean integration with v1.0.0 plotting functions

- **Configuration System**
  - PlotSpec configuration with YAML support
  - Factory methods: `from_yaml()`, `from_file()`, `from_dict()`
  - Clean `to_dict()` export method for programmatic configuration
  - Pydantic validation with proper error messages

### Changed
- **API Simplification** (Breaking Changes)
  - Unified API reduced to 4 core components: `PlotSpec`, `plot()`, `load_spice_raw()`, `WaveDataset`
  - Single import pattern: `import wave_view as wv`
  - Explicit data flow: load → configure → plot → show
  - Clean separation between configuration (PlotSpec) and visualization (plotting functions)
  - Direct signal lookup without complex resolution layers

- **Data Loading Interface** (Breaking Changes)
  - `load_spice_raw()` returns Dict[str, np.ndarray] format instead of custom classes
  - Simple dictionary interface for signal access
  - WaveDataset as the only data loading mechanism
  - Metadata support for simulation information (future features)

See documentation for detailed examples with the new API.

## [0.1.0] - 2025-06-10

### Added
- **Core Package Implementation**
  - Complete SPICE waveform visualization package
  - `SpiceData` class with case-insensitive signal access
  - `PlotConfig` class with YAML configuration support
  - `SpicePlotter` class with advanced plotting features
  - Simple `plot()` API for quick visualization

- **Interactive Plotting**
  - Plotly-based interactive visualizations
  - Zoom, pan, and hover capabilities
  - Auto-configuration from SPICE files
  - Fixed zoom XY functionality for proper axis reset

- **Configuration System**
  - YAML-based plotting configurations
  - Template generation from SPICE files
  - Configuration validation with helpful warnings
  - Support for file, dictionary, and string configs
  - Factory functions: `config_from_file()`, `config_from_yaml()`, `config_from_dict()`

- **Advanced Features**
  - Processed signal generation with lambda functions
  - Case-insensitive signal name matching
  - Jupyter notebook integration with auto-detection
  - Manual renderer control for different environments
  - AC simulation complex number support for transfer function analysis

- **UI Polish**
  - Center-aligned plot titles by default
  - Configurable title positioning (`title_x`, `title_xanchor`)
  - Fixed zoom button functionality
  - Professional plot appearance

- **Project Infrastructure**
  - Modern Python packaging with `pyproject.toml`
  - Comprehensive test suite (234 tests, 91% coverage)
  - MIT License for open source distribution
  - Professional repository structure with src/ layout
  - Complete Sphinx documentation
  - GitHub Actions CI/CD pipeline
  - PyPI publication ready

### Removed
- **Multi-figure Support** (Breaking Change)
  - Removed `is_multi_figure`, `figure_count`, and `get_figure_config()` methods from `PlotConfig`
  - YAML list configurations now raise helpful error messages with migration guidance
  - Users should create separate configurations and call `plot()` multiple times instead
  - Simplifies API and reduces maintenance complexity

### Fixed
- **AC Simulation Complex Numbers**: Fixed dtype casting that was discarding imaginary parts
- **Zoom XY Button**: Properly resets axis fixedrange properties for free zooming
- **Signal Parsing**: Improved robustness for various SPICE file formats

### Project Structure
- Reorganized for PyPI publication
- Moved to src/ layout following Python packaging best practices
- Consolidated tests, examples, and documentation
- Added development dependencies and tooling

### Testing
- 234 comprehensive unit and integration tests
- Real SPICE data validation
- Coverage reporting setup
- Pytest configuration with modern tooling

## [0.0.1] - 2025-06-05 (Initial Prototype)

### Added
- Initial project structure
- Basic class framework
- Development environment setup
- Proof of concept implementation

---

## Legend

- **Added**: New features
- **Changed**: Changes in existing functionality  
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Vulnerability fixes 