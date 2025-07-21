# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-07-21

### 🚨 BREAKING CHANGES
- **Package Rename**: `wave_view` → `yaml2plot` to avoid trademark collision with Synopsys WaveView
- **CLI Command Change**: `waveview` → `y2p` for improved user experience
- **Import Updates**: All imports now use `import yaml2plot as y2p`

### Changed
- **Package Name**: Complete rename from wave_view to yaml2plot across all components
- **CLI Interface**: New `y2p` command replaces `waveview` for all operations
- **Module Structure**: All internal modules updated to yaml2plot namespace
- **Documentation**: Updated all examples and documentation to use new naming

### Migration Guide
For existing users upgrading from wave_view:

**Python Code**:
```python
# Old (v1.x)
import wave_view as wv
data, metadata = wv.load_spice_raw("file.raw")

# New (v2.0.0)
import yaml2plot as y2p
data, metadata = y2p.load_spice_raw("file.raw")
```

**CLI Usage**:
```bash
# Old (v1.x)
waveview init simulation.raw
waveview plot config.yaml

# New (v2.0.0)
y2p init simulation.raw
y2p plot config.yaml
```

### Technical Details
- All 149+ import statements updated across codebase
- 61 tests passing with 90% coverage maintained
- Full backward API compatibility within yaml2plot namespace
- No functional changes to core plotting or data loading capabilities

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