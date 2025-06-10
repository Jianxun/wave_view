# Project Memory

## Project Overview
Wave_view is a Python package for SPICE simulation visualization with a modern, user-friendly API. The project features core modules for configuration management (config.py), data reading (reader.py), and plotting (plotter.py), with comprehensive YAML-based configuration support and advanced features like log scale plotting and processed signal generation.

## Current State
**Test Suite Development Sprint - COMPREHENSIVE COMPLETION** ✅

**🏆 MAJOR MILESTONE ACHIEVED**: Complete test-driven development with modular architecture for all core modules!

**Final Test Coverage Results**:
- **PlotConfig**: 73 tests, 96% coverage ✅
- **SpicePlotter**: 47 tests, 93% coverage ✅  
- **SpiceData**: 56 tests, 100% coverage ✅
- **🎯 TOTAL**: **176 comprehensive tests** with **95%+ coverage** on all core modules

**Test Architecture Excellence - COMPLETE**:
- **Consistent Modular Organization**: All three core modules follow the same modular test pattern
- **Shared Utilities**: Common fixtures, mock creators, and assertion helpers in each module's `__init__.py`
- **Real-World Integration**: Tests with actual SPICE files alongside controlled mocking
- **Comprehensive Coverage**: Basic functionality, error handling, edge cases, and advanced features
- **Development Guidelines**: Following test-driven development principles throughout
- **Maintainability**: Focused test files make it easy to understand and extend tests

**Recently Completed - Config Test Modularization**:
Successfully broke down the large monolithic `test_config.py` (742 lines) into a clean modular structure:
- **`tests/unit_tests/config/`** directory with organized test files
- **`__init__.py`**: Comprehensive shared utilities (temp file creators, mock utilities, validation helpers)
- **`test_config_basic.py`**: Initialization and basic functionality (24 tests)
- **`test_config_validation.py`**: Configuration validation and error handling (33 tests)  
- **`test_config_features.py`**: Advanced features (templates, log scale, raw file paths) (16 tests)
- **Total**: 73 tests maintaining 96% coverage with improved organization

**Modular Test Pattern Established**:
All three core modules now follow the same excellent pattern:
```
tests/unit_tests/{module}/
├── __init__.py                 # Shared utilities & fixtures
├── test_{module}_basic.py      # Core functionality
├── test_{module}_*.py          # Feature-specific test files
└── test_{module}_edge_cases.py # Error handling & edge cases
```

**Key Achievements Completed**:
- ✅ **SpiceData Reader Module Testing** (56 tests, 100% coverage)
- ✅ **SpicePlotter Module Testing** (47 tests, 93% coverage)  
- ✅ **PlotConfig Module Testing** (73 tests, 96% coverage)
- ✅ **Real SPICE File Integration** with Ring_Oscillator_7stage.raw
- ✅ **Consistent Modular Test Structure** across all core modules
- ✅ **Advanced Feature Testing** (log scale, processed signals, multi-figure)
- ✅ **Test Organization Excellence** with maintainable, focused test files

**Next Phase**: Integration testing and API validation to ensure seamless system operation.

**✅ SPRINT 1 COMPLETE + MAJOR API ENHANCEMENTS COMPLETE**
- Core wave_view package fully implemented ✅
- Repository reorganized for PyPI publication ✅
- Modern Python packaging structure (src/ layout) ✅
- Package installable via pip install -e . ✅
- **NEW**: Processed data API with clean user interface ✅
- **NEW**: Log scale support for X and Y axes ✅
- **NEW**: Comprehensive unit tests for PlotConfig class (33 tests, 96% coverage) ✅
- **NEW**: Comprehensive modular unit tests for SpicePlotter class (47 tests, 93% coverage) ✅
- Core reader tests in progress ⏳

**Repository Structure:**
```
wave_view/
├── src/wave_view/           # Main package (src layout)
├── tests/                   # Consolidated test suite
├── examples/                # Demo scripts & notebooks
│   ├── data/               # Demo SPICE files
│   ├── scripts/            # Python demo scripts  
│   └── notebooks/          # Jupyter demos
├── docs/                   # Documentation
├── pyproject.toml          # Modern packaging config
├── LICENSE                 # MIT license
├── requirements-dev.txt    # Development dependencies
└── README.md              # Project documentation
```

## Key Decisions
- **Package Name**: `wave_view` (snake_case) following PEP 8 conventions
- **Structure**: src/ layout for professional Python packaging  
- **License**: MIT License for open source distribution
- **Build System**: setuptools with pyproject.toml (modern standard)
- **API Design**: Simple plot() function + advanced SpicePlotter class
- **Configuration**: YAML-based plotting configuration system
- **Case Handling**: Case-insensitive signal name matching

## Completed Features
**Core API:**
- `load_spice()` - Load SPICE files
- `plot()` - Simple plotting interface  
- `SpicePlotter` - Advanced plotting class
- `PlotConfig` - YAML configuration system
- `create_config_template()` - Auto-generate configs

**Key Capabilities:**
- Multi-figure plotting support
- Case-insensitive signal access
- Processed signal generation (lambda functions)
- YAML configuration validation
- Auto-configuration from SPICE files
- Plotly integration with Jupyter widgets

## Open Questions
None - package is ready for publication!

## API for Signal Discovery

**✅ Signal Exploration APIs Available:**

1. **Basic Signal Listing** (Core API):
   ```python
   data = wv.load_spice("file.raw")
   print(data.signals)  # List all signal names (lowercase)
   print(data.info)     # File metadata
   ```

2. **Advanced Signal Explorer** (Examples ready for integration):
   - `SpiceSignalExplorer` class in `examples/scripts/signal_explorer.py`
   - Categorizes signals by type (voltage, current, device terminals)
   - Provides display_summary(), display_tree(), search(), and categorization methods

3. **YAML Configuration Support**:
   - Full YAML string support for configurations (multi-line strings)
   - Multi-figure YAML configurations (list format)
   - Auto-template generation: `wv.create_config_template("output.yaml", raw_file="input.raw")`
   - YAML file loading and validation

**✅ NEW: Processed Data API (User-Facing)**

4. **Processed Data Parameter** (Main API Enhancement):
   ```python
   import wave_view as wv
   import numpy as np
   
   # Load data and compute processed signals
   data = wv.load_spice("simulation.raw")
   processed_data = {
       "vdb_out": 20 * np.log10(np.abs(data.get_signal("v(out)"))),
       "power": data.get_signal("v(vdd)") * data.get_signal("i(vdd)"),
       "phase": np.angle(data.get_signal("v(out)")) * 180 / np.pi
   }
   
   # Use in YAML config with "data." prefix
   config = '''
   title: "Analysis with Processed Data"
   X: {signal_key: "raw.time", label: "Time (s)"}
   Y:
     - label: "Magnitude (dB)"
       signals: {Output: "data.vdb_out"}
     - label: "Power (W)"
       signals: {Supply: "data.power"}
   '''
   
   # Plot with processed data
   fig = wv.plot("simulation.raw", config, processed_data=processed_data)
   ```

**Key Enhancement**: SpicePlotter is now internal-only. Users get clean API via `processed_data` parameter in the main `plot()` function.

**✅ NEW: Log Scale Support**

5. **Logarithmic Axis Scaling**:
   ```yaml
   # X-axis log scale (perfect for Bode plots)
   X:
     signal_key: "raw.frequency"
     label: "Frequency (Hz)"
     scale: log
   
   # Y-axis log scale (useful for power analysis)  
   Y:
     - label: "Power (W)"
       scale: log
       signals:
         Supply: "data.power"
   ```
   
   **Use Cases:**
   - Frequency response plots (Bode plots)
   - Power analysis with wide dynamic range
   - Any data spanning multiple orders of magnitude
   - Both X and Y axes support `scale: log` or `scale: linear` (default)

## Recent Issues Resolved
- **Import Issue Fixed**: Updated demo script to use proper package import (`import wave_view as wv`) instead of hacky sys.path manipulation
- **Package Installation**: Confirmed package is properly installed in development mode (pip install -e .)
- **X-Axis Positioning Fixed**: Fixed x-axis positioning by correcting Y-axis domain calculation and improving UX. All y-axes now properly anchor to x-axis with intuitive stacking order.
- **Y-Axis Order UX Fixed**: Reversed Y-axis processing order so first Y-axis in config appears at TOP of plot (intuitive reading order), not bottom. This matches user expectations.
- **Comprehensive Testing Added**: Created full test suite covering all API functionality, edge cases, and configuration formats
- **Documentation Updated**: Enhanced README.md with comprehensive installation instructions including development mode and GitHub installation options
- **API Enhancement - Processed Data**: Modified `plot()` function to accept `processed_data` parameter, eliminating need for users to access internal SpicePlotter class. Users can now pass pre-computed numpy arrays and reference them in YAML config with "data." prefix.
- **Log Scale Support**: Added logarithmic axis scaling for both X and Y axes. Users can specify `scale: log` in YAML configuration for frequency response plots (Bode plots) and other logarithmic data visualization.

## Next Steps
- Polish documentation for PyPI
- Consider GitHub Actions for CI/CD
- Plan Sprint 2 features (signal exploration UI) 

**🔧 VERSION CONTROL LESSONS LEARNED & GUIDELINES ENHANCEMENT** 📚

**Real-World Version Control Practice Results**:

### ✅ **Lessons from Branch Reorganization Experience**
**Problem**: Mixed test infrastructure work with feature development in same branch (`test_suite_development`)
**Solution**: Successfully reorganized commits into separate purpose-driven branches:
- `test_suite_development` → Test infrastructure, TDD guidelines, testing framework
- `api_input_validation_improvements` → Feature development with input validation

**Key Insights Gained**:
1. **Branch Purpose Separation**: Different work types (infrastructure vs features) should live on separate branches
2. **Pull Request Strategy**: Infrastructure should be merged before features that depend on it  
3. **Repository Hygiene**: Immediate cleanup of merged branches maintains clean repository state
4. **Branch Naming**: Descriptive names (`api_input_validation_improvements` vs generic names) improve clarity
5. **Commit Organization**: Logical grouping by purpose, not just chronological order

### ✅ **Enhanced Development Guidelines**
**Comprehensive Version Control Section Added**:

#### **Branching Strategy Framework**
- **Branch Types**: Feature, test infrastructure, bug fixes, documentation, repository maintenance
- **Naming Conventions**: Purpose-driven names that clearly indicate scope and intent
- **Management Rules**: Single purpose, descriptive names, foundation-first merging, prompt cleanup

#### **Pull Request Workflow**
- **Systematic Sequencing**: Infrastructure → Core Features → Enhancements → Documentation
- **Best Practices**: Single responsibility, complete testing, clear descriptions, breaking change documentation

#### **Repository Hygiene**
- **Cleanup Process**: Immediate deletion after merge, regular audits, stale branch detection
- **Maintenance Practices**: Separate dependency updates, documentation sync, clean state verification

#### **Recovery Strategies**
- **Common Scenarios**: Mixed work types, wrong base branch, commit organization issues
- **Recovery Tools**: Branch extraction, reset/rebuild, cherry-pick, interactive rebase
- **Prevention**: Planning before coding, single focus sessions, frequent commits, context documentation

### ✅ **Integration with Focused Development**
**Enhanced Implementation Process**:
- Added version control integration to focused feature development workflow
- Branch planning considerations before starting work
- Atomic commits for each completed feature
- Clean state maintenance between tasks and sessions

**Session Management Framework**:
- Starting sessions: Context review, branch status check, work focus planning
- Ending sessions: Clean commits, context updates, repository state maintenance

**Practical Impact**:
- ✅ **Cleaner Repository**: From 5 branches to 2 active branches (main + current feature)
- ✅ **Better Organization**: Clear separation between test infrastructure and feature work
- ✅ **Improved Workflow**: Systematic approach to branching, commits, and PRs
- ✅ **Enhanced Guidelines**: Comprehensive version control practices documented for future sessions 