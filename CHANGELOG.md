# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Removed
- **Multi-figure Support** (Breaking Change)
  - Removed `is_multi_figure`, `figure_count`, and `get_figure_config()` methods from `PlotConfig`
  - YAML list configurations now raise helpful error messages with migration guidance
  - Users should create separate configurations and call `plot()` multiple times instead
  - Simplifies API and reduces maintenance complexity

### Planned
- GitHub Actions CI/CD pipeline
- Comprehensive documentation site
- PyPI publication
- Signal exploration UI (Sprint 2)

## [0.1.0] - 2024-01-XX (Current Alpha)

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

- **Configuration System**
  - YAML-based plotting configurations
  - Template generation from SPICE files
  - Configuration validation with helpful warnings
  - Support for file, dictionary, and string configs

- **Advanced Features**
  - Processed signal generation with lambda functions
  - Case-insensitive signal name matching
  - Jupyter notebook integration with auto-detection
  - Manual renderer control for different environments

- **Project Infrastructure**
  - Modern Python packaging with `pyproject.toml`
  - Comprehensive test suite (18 tests)
  - MIT License for open source distribution
  - Professional repository structure with src/ layout

### Project Structure
- Reorganized for PyPI publication
- Moved to src/ layout following Python packaging best practices
- Consolidated tests, examples, and documentation
- Added development dependencies and tooling

### Testing
- 18 comprehensive unit and integration tests
- Real SPICE data validation
- Coverage reporting setup
- Pytest configuration with modern tooling

## [0.0.1] - 2024-01-XX (Initial Prototype)

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