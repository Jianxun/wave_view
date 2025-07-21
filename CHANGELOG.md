# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.1] - 2025-07-19

### Documentation
- Updated all documentation links in README and CLI help to point to the new GitHub Pages site.
- Improved clarity and accuracy of help messages.

## [1.1.0] - 2025-07-19

### Added
- **CLI Enhancements**: Introduced `y2p init` subcommand for generating plot specifications, streamlined `y2p plot` for easier usage, and added regex filtering to `y2p signals` for better signal discovery.

### Improved
- **User Experience**: Enhanced CLI user experience with clearer command usage and improved help text.

### Documentation
- **Documentation Updates**: Improved documentation structure and added comprehensive examples for all CLI commands and options.

## [1.0.1] - 2025-07-11

### Fixed
- Minor bug fixes and improvements.

## [1.0.0] - 2025-07-11

### Added
- **Modern API Architecture**: Complete redesign with `PlotSpec`, `WaveDataset`, `plot()`, `load_spice_raw()`.
- **Command Line Interface**: Updated CLI to use v1.0.0 API.
- **Configuration System**: PlotSpec configuration with YAML support.

### Changed
- **API Simplification**: Unified API, single import pattern, explicit data flow.
- **Data Loading Interface**: `load_spice_raw()` returns Dict format.

## [0.1.0] - 2025-06-10

### Added
- **Core Package Implementation**: SPICE waveform visualization package.
- **Interactive Plotting**: Plotly-based visualizations.
- **Configuration System**: YAML-based configurations.

### Removed
- **Multi-figure Support**: Simplified API.

### Fixed
- **AC Simulation Complex Numbers**: Fixed dtype casting.

## [0.0.1] - 2025-06-05 (Initial Prototype)

### Added
- Initial project structure, basic class framework, development environment setup.

---

## Legend

- **Added**: New features
- **Changed**: Changes in existing functionality  
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Vulnerability fixes 