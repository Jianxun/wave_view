# Project Todo List

## Current Sprint - Version 0.2.0 Phase 1 Development ✅ **MAJOR PROGRESS**

### 📋 **Development Methodology and Lessons Learned**

#### **TDD Success Story** ✅ **METHODOLOGY VALIDATION**
- **Approach**: Strict one-test-at-a-time TDD following development guidelines
- **Process**: Red → Green → Refactor cycle with immediate test verification
- **Quality Results**: 93% PlotSpec coverage, 66% SpicePlotter coverage improvement
- **Key Lesson**: TDD discipline prevents feature creep and ensures robust implementation

#### **Pydantic Integration Benefits** ✅ **ARCHITECTURAL SUCCESS**
- **Validation**: Automatic validation with rich error messages
- **Type Safety**: IDE autocompletion and type checking
- **Maintenance**: Self-documenting code with Field descriptions
- **Future**: Foundation for JSON schema generation and editor support

#### **Session Accomplishments** ✅ **WaveDataset TDD Success**
1. **WaveDataset Implementation**: Complete modern data container replacing SpiceData
2. **TDD Methodology**: Strict Red-Green-Refactor cycle with 9 comprehensive tests
3. **Package Integration**: Properly exported WaveDataset in main package API
4. **80% Test Coverage**: High-quality implementation with edge case handling

#### **Next Session Priorities**
1. **API Integration**: Create wrapper functions for backward compatibility
2. **Demo Updates**: Update examples to showcase new v0.2.0 API patterns
3. **Phase 2 Prep**: Begin HTML Report Builder or continue with API integration
4. **Documentation**: Update examples and quickstart with new WaveDataset API

## Previous Sprint - Release 0.1.0 ✅ **SUCCESSFULLY PUBLISHED**

### 🚀 **Release 0.1.0 Final Steps** ✅ **COMPLETED**
- [X] **Update CHANGELOG.md** ✅ **COMPLETED**
  - Updated release date to 2024-12-19
  - Moved all unreleased features to 0.1.0 section
  - Added comprehensive feature list and breaking changes documentation
  - Added Fixed section with bug fixes and improvements

- [X] **Build and Validate Package** ✅ **COMPLETED**
  - Successfully built clean distribution files (wheel + sdist)
  - Passed twine check validation for PyPI compatibility
  - Verified package installation and import functionality
  - All 234 tests passing with 91% coverage

- [X] **Update Context Documentation** ✅ **COMPLETED**
  - Updated project memory with release 0.1.0 status
  - Documented package quality and readiness for publication
  - Updated current state to reflect main branch and clean working tree

### 🎉 **PyPI Publication** ✅ **SUCCESSFULLY COMPLETED**
- [X] **Setup Trusted Publishing** ✅ **COMPLETED**
  - Configured PyPI trusted publisher for automated GitHub Actions publishing
  - No API tokens required - secure OIDC authentication

- [X] **GitHub Release Created** ✅ **COMPLETED**
  - Created GitHub release from v0.1.0 tag
  - Triggered automated PyPI publishing workflow
  - GitHub Actions successfully built and uploaded package

- [X] **PyPI Publication Verified** ✅ **COMPLETED**
  - Package available at: https://pypi.org/project/wave-view/
  - Clean installation: `pip install wave_view` ✅ Working
  - Version verification: `wave_view.__version__ == "0.1.0"` ✅ Correct
  - API functions available: All 13 main functions properly exported ✅
  - Dependencies installed correctly: plotly, numpy, PyYAML, spicelib ✅

### 📊 **Release 0.1.0 Final Status**: Successfully published to PyPI and fully verified ✅ **SUCCESS**

### 📋 **Ready for Release Actions** (USER ACTION REQUIRED)
- [ ] **Create Release Tag**: `git tag -a v0.1.0 -m "Release version 0.1.0"`
- [ ] **Push Release Tag**: `git push origin v0.1.0`
- [ ] **GitHub Release**: Create GitHub release from tag (will trigger PyPI publish via Actions)
- [ ] **Verify PyPI Publication**: Confirm package appears on PyPI after Actions complete

### 📊 **Release 0.1.0 Status**: Package built, tested, and ready for publication ✅ **SUCCESS**

## Next Sprint - Version 0.2.0 Architecture Implementation

### 🎯 **Version 0.2.0 Phase 1: Core API Refactoring** (HIGH PRIORITY) 🚀 **IN PROGRESS**

#### **PlotSpec Implementation** ✅ **COMPLETED**
- [X] **Create PlotSpec Class with Pydantic Validation** ✅ **COMPLETED**
  - Created `PlotSpec` and `YAxisSpec` Pydantic models in `src/wave_view/core/plotspec.py`
  - Implemented comprehensive validation with Field descriptions
  - Added type safety with proper Union types and Optional fields
  - Achieved 93% test coverage with systematic TDD approach

- [X] **Implement Core PlotSpec Methods** ✅ **COMPLETED**
  - `PlotSpec.from_yaml()` - Factory method with YAML parsing and error handling
  - `PlotSpec.plot(data)` - Core plotting method returning Plotly figures
  - Multi-axis Y configuration support (tested with real configs from demo_ota_5t.py)
  - Integration with existing SpicePlotter infrastructure

- [X] **Add Pydantic Configuration Validation** ✅ **COMPLETED**
  - Replaced ad-hoc validation with structured Pydantic models
  - Rich validation error messages with field-level details
  - Type hints for improved developer experience
  - Added pydantic>=2.0.0 to requirements.txt

#### **Phase 1 Completed Tasks** ✅ **COMPLETED**
- [X] **Complete PlotSpec API** ✅ **COMPLETED**
  - Added `PlotSpec.from_file()` method for YAML file loading
  - Added `PlotSpec.show()` method for direct figure display
  - Added `PlotSpec.get_figure()` method for Plotly figure access
  - Updated main `__init__.py` to export PlotSpec
  - All 10 tests passing with comprehensive coverage
  - Demo script verified working as Jupyter notebook

- [X] **Simple WaveDataset Implementation** ✅ **COMPLETED**
  - Created minimal `WaveDataset` class for single-figure plotting
  - Implemented `WaveDataset.from_raw()` with optional metadata support
  - Added essential methods: `signals`, `get_signal()`, `has_signal()`, `metadata`
  - Full case-insensitive signal handling with proper error messages
  - Package integration: Available as `import wave_view as wv; wv.WaveDataset`
  - 9 comprehensive tests, 80% coverage achieved
  - Modern replacement for `SpiceData` with backward compatibility maintained

#### **Next Phase 1 Tasks** (HIGH PRIORITY)
- [ ] **API Integration and Backward Compatibility**
  - Create wrapper functions to maintain existing `wv.plot()` API
  - Ensure seamless migration path for existing users
  - Update examples to showcase new API alongside old API

#### **Testing and Documentation** (HIGH PRIORITY)
- [X] **Expand Test Coverage** ✅ **COMPLETED**
  - Added tests for `from_file()` method and file I/O edge cases
  - Added tests for `show()` and `get_figure()` methods
  - Added integration tests for PlotSpec with SpiceData
  - Achieved comprehensive test coverage for all new methods

- [X] **Fix Demo Script Integration** ✅ **COMPLETED**
  - Demo script verified working as Jupyter notebook
  - PlotSpec successfully imported and used from main package
  - End-to-end workflow with real SPICE data confirmed working

### 🎯 **Version 0.2.0 Phase 2: HTML Report Builder** (HIGH PRIORITY)
- [ ] **Create ReportSpec Pydantic Model**
  - Design declarative report configuration format
  - Support sections, headings, notes, and multiple figures
  - Include theme support and metadata fields
  - Validate report structure at load time

- [ ] **Implement ReportBuilder Class**
  - Create Jinja2 template system for HTML generation
  - Support self-contained HTML with embedded Plotly JSON
  - Add CDN vs inline Plotly.js options
  - Handle figure collection and HTML assembly

- [ ] **Add CLI Command for Reports**
  - Implement `wave_view report report.yaml --out report.html`
  - Support metadata file input for sweep data
  - Add options for PDF export and theme selection
  - Provide comprehensive help and examples

### 🎯 **Version 0.2.0 Phase 3: Foundation for Parameter Sweeps** (MEDIUM PRIORITY)
- [ ] **WaveDataset with Metadata Support**
  - Create `WaveDataset` class to hold signals + metadata
  - Support `from_raw()` with optional metadata dict
  - Enable metadata-driven legend templating
  - Prepare for multi-file collection support

- [ ] **DataFrame-based Metadata Operations**
  - Implement `slice_df()` and `group_df()` helper functions
  - Support filtering: `slice: {temperature: 85, corner: tt}`
  - Enable grouping: `group: [temperature, corner]`
  - Add legend templating: `"{corner}_{temperature}°C"`

### 🎯 **Version 0.3.0 Planning: Full Parameter Sweep Engine** (FUTURE)
- [ ] **Multi-File Collection Support**
  - `WaveDataCollection` class for multiple raw files
  - Statistical aggregators (envelope, mean, percentiles)
  - Continuous color mapping for parameter sweeps
  - Monte Carlo analysis with confidence bands

- [ ] **Advanced Sweep Visualization**
  - PVT corner overlay plots
  - Parameter sweep with color coding
  - Statistical summary tables
  - Interactive parameter exploration

### 🎯 **Version 0.1.1 Maintenance** (LOW PRIORITY)
- [ ] **Monitor Initial Users**: Gather feedback and bug reports
- [ ] **Documentation Site**: Consider hosting documentation (e.g., GitHub Pages, Read the Docs)
- [ ] **Performance Optimization**: Profile and optimize for large SPICE files
- [ ] **Additional Plot Types**: Expand visualization options based on user needs

## Current Sprint - PyPI Release Preparation ✅ **COMPLETED**

### 📦 **PyPI Release Preparation** (HIGH PRIORITY) ✅ **COMPLETED**
- [X] **Update Package Metadata** ✅ **COMPLETED**
  - Updated author information in pyproject.toml (Jianxun Zhu)
  - Modernized license format to SPDX "MIT" instead of deprecated table format
  - Removed deprecated license classifier
  - Updated GitHub URLs to correct repository paths

- [X] **Add Type Information Support** ✅ **COMPLETED**
  - Created py.typed marker file for type information distribution
  - Configured pyproject.toml to include py.typed in package data

- [X] **Setup CI/CD Infrastructure** ✅ **COMPLETED**
  - Added GitHub Actions workflow for automated PyPI publishing on releases
  - Added comprehensive test workflow for Python 3.8-3.12 with coverage reporting
  - Configured trusted publishing for secure PyPI uploads

- [X] **Branch and Commit Changes** ✅ **COMPLETED**
  - Created `pypi_release_preparation` branch for release changes
  - Committed all PyPI preparation work with comprehensive commit message
  - Ready for merge to main and PyPI publication

### 📊 **PyPI Release Status**: Package ready for publication with professional packaging standards ✅ **SUCCESS**

## Previous Sprint - Documentation Configuration Update ✅ **COMPLETED**

### 📚 **Sphinx Documentation Configuration Format Update** (HIGH PRIORITY) ✅ **COMPLETED**
- [X] **Update Quickstart Guide** ✅ **COMPLETED**
  - Replaced dictionary `plots` format with YAML `X`/`Y` axis structure
  - Updated all code examples to use `config_from_yaml()` function
  - Modernized configuration examples with proper signal references

- [X] **Update Index Page** ✅ **COMPLETED**
  - Updated quick start example to use correct YAML format
  - Replaced dictionary configuration with `config_from_yaml()` usage

- [X] **Update Configuration Guide** ✅ **COMPLETED**
  - Completely rewrote configuration structure documentation
  - Added comprehensive X/Y axis configuration options
  - Updated all examples to use current API format
  - Documented signal reference patterns (raw.signal, data.signal)

- [X] **Update Examples Documentation** ✅ **COMPLETED**
  - Updated all 8+ examples to use YAML configuration format
  - Replaced dictionary configurations with `config_from_yaml()` calls
  - Modernized signal references and axis configurations
  - Updated multi-figure and processed data examples

- [X] **Build and Verify Documentation** ✅ **COMPLETED**
  - Successfully built HTML documentation with updated examples
  - Verified all configuration examples use correct format
  - Documentation builds cleanly with only minor autosummary warnings

- [X] **Simplify Signal References** ✅ **COMPLETED**
  - Removed all `raw.` prefixes from signal references in documentation
  - Updated signal_key examples: `raw.time` → `time`, `raw.frequency` → `frequency`
  - Updated signal reference documentation to show simplified format
  - Verified documentation builds successfully with simplified references

### 📊 **Documentation Status**: All examples updated to current YAML X/Y format with simplified signal references ✅ **SUCCESS**

## Previous Sprint - Documentation Setup ✅ **COMPLETED**

### 📚 **Sphinx Documentation** (HIGH PRIORITY) ✅ **COMPLETED**
- [X] **Install Sphinx Dependencies** ✅ **COMPLETED**
  - Installed sphinx, sphinx-rtd-theme, myst-parser from docs optional dependencies
  - All documentation tools now available in development environment

- [X] **Initialize Sphinx Configuration** ✅ **COMPLETED**
  - Created comprehensive `docs/conf.py` with proper extensions
  - Configured autodoc, autosummary, napoleon, intersphinx, myst-parser
  - Set up Read the Docs theme with proper navigation options
  - Added Python path configuration for package discovery

- [X] **Create Documentation Structure** ✅ **COMPLETED**
  - `index.rst` - Main documentation page with feature overview
  - `installation.rst` - Installation guide with all dependency options
  - `quickstart.rst` - 3-step workflow tutorial with examples
  - `configuration.rst` - Comprehensive configuration guide
  - `examples.rst` - Practical examples for common use cases
  - `api.rst` - API reference with autosummary
  - `core.rst` - Core modules documentation
  - `changelog.rst` - Version history and changes
  - `contributing.rst` - Development and contribution guide

- [X] **Build and Test Documentation** ✅ **COMPLETED**
  - Successfully built HTML documentation with Sphinx
  - Fixed autosummary extension configuration
  - Resolved API reference issues (removed non-existent functions)
  - Documentation builds cleanly with only minor warnings
  - Generated comprehensive API documentation with cross-references

### 📊 **Documentation Status**: Complete HTML documentation generated ✅ **SUCCESS**

## Current Sprint - Fix Broken Tests (URGENT) ✅ **COMPLETED**

### 🚨 **Test Failures from API Changes** (HIGH PRIORITY) ✅ **ALL FIXED**
- [X] **Fix PlotConfig Constructor Tests** (11 tests failing) ✅ **COMPLETED**
  - Updated tests in `test_config_basic.py` (8 tests), `test_basic.py` (2 tests), `test_config_features.py` (3 tests)
  - Replaced string parameter tests with explicit config_from_file() calls
  - Removed tests for removed auto-detection functionality

- [X] **Fix plot() Function API Tests** (4 tests failing) ✅ **COMPLETED**
  - Updated `test_api_plot.py` (2 tests) and `test_path_support.py` (2 tests)
  - Replaced file path parameters with config_from_file() usage
  - Updated mock expectations to match new PlotConfig object behavior

- [X] **Remove plot_batch Tests** (8 tests failing) ✅ **COMPLETED**
  - Deleted `test_plot_batch.py` entirely
  - Function was removed from API for simplification
  - Updated any integration tests that referenced plot_batch()

- [X] **Fix Internal Method Tests** (4 tests failing) ✅ **COMPLETED**
  - Removed TestFilePathDetection class from `test_config_basic.py`
  - `_looks_like_file_path()` method was removed with auto-detection logic
  - Cleaned up tests that relied on internal implementation details

- [X] **Fix Type Import Issues** (1 test failing) ✅ **COMPLETED**
  - Fixed isinstance() call in `test_path_support.py::test_all_functions_accept_path_objects`
  - Resolved PlotConfig import/typing issue in api.py
  - Ensured proper type checking across API

### 📊 **Test Status**: 226 passing, 0 failing (100% pass rate) ✅ **SUCCESS**

## Current Sprint - Code Quality & Polish ✅ **COMPLETED**

### 🔧 **Code Organization & Quality** (High Priority) ✅ **ALL COMPLETED**
- [X] **Extract Signal Categorization Utility** 
  - Location: `src/wave_view/api.py:285-300` in `explore_signals()`
  - ✅ **COMPLETED**: Created reusable `_categorize_signals()` utility function
  - Replaced hardcoded logic with clean, testable utility
  - Function returns tuple of (voltage_signals, current_signals, other_signals)

- [X] **Replace Magic Numbers with Named Constants**
  - Location: `src/wave_view/core/reader.py:95-96` 
  - ✅ **COMPLETED**: Added `MAX_SIGNALS_TO_SHOW = 5` constant
  - Replaced hardcoded `[:5]` with named constant for better maintainability

- [X] **Add Missing Type Annotations**
  - Location: `src/wave_view/api.py:145-166`
  - ✅ **COMPLETED**: Added type hints to internal functions
  - `_configure_plotly_renderer() -> None` and `_is_jupyter_environment() -> bool`
  - Consistent type annotation across all functions

## Current Sprint - UI Polish Improvements ✅ **COMPLETED**

### 🎨 **UI Polish Tasks** (HIGH PRIORITY) ✅ **ALL COMPLETED**

- [X] **Fix Zoom XY Functionality** ✅ **COMPLETED**
  - Fixed broken Zoom XY button that only set dragmode without resetting fixedrange properties
  - Now properly resets both X and Y axis fixedrange to False for free zooming
  - Verified all zoom buttons work correctly (Zoom XY, Zoom Y, Zoom X)

- [X] **Implement Center Title Alignment** ✅ **COMPLETED**
  - Added default center alignment for plot titles (x=0.5, xanchor=center)
  - Replaced old title_text with structured title configuration
  - Improved visual consistency with centered titles by default

- [X] **Add Configurable Title Alignment** ✅ **COMPLETED**
  - Added `title_x` configuration option (0.0=left, 0.5=center, 1.0=right)
  - Added `title_xanchor` configuration option ("left", "center", "right")
  - Provides full flexibility for custom title positioning
  - Maintains backward compatibility with existing configurations

- [X] **Comprehensive Test Coverage** ✅ **COMPLETED**
  - Created `test_plotter_ui_polish.py` with 8 comprehensive tests
  - Tests cover zoom functionality, title alignment, and integration scenarios
  - All 228 tests pass with 92% coverage maintained
  - Verified no regressions in existing functionality

### 📊 **UI Polish Status**: All identified issues resolved ✅ **SUCCESS**

## Current Sprint - AC Simulation Complex Number Fix ✅ **COMPLETED**

### 🔧 **AC Simulation Complex Number Parsing** ✅ **FIXED**
- [X] **Investigate AC Simulation Data Parsing** ✅ **COMPLETED**
  - Issue: AC simulation "v(out)" was returning real numbers instead of complex numbers
  - Root Cause: `dtype=float` parameter in `reader.py` line 118 was forcing conversion and discarding imaginary parts
  - Solution: Removed dtype constraint to preserve original spicelib data types

- [X] **Fix Implementation** ✅ **COMPLETED**
  - Fixed `src/wave_view/core/reader.py` get_signal() method to preserve complex numbers
  - Updated test utility `assert_signal_data_integrity()` to handle both real and complex dtypes
  - Added comprehensive test suite `test_reader_complex_numbers.py` with 6 test cases
  - Verified magnitude/phase calculations work correctly for transfer function analysis

### 📋 **Investigation Tasks** ✅ **ALL COMPLETED**
- [X] Examined SPICE raw file format for AC analysis results (contains `Flags: complex`)
- [X] Checked reader.py parsing logic for complex number handling (found dtype=float bug)
- [X] Verified AC vs transient analysis data type handling (both work correctly now)
- [X] Tested with actual AC simulation files (tb_ota_5t AC results working perfectly)
- [X] Ensured magnitude and phase calculations work correctly (✅ verified with real data)

### 📊 **Fix Results**: AC analysis with complex numbers fully functional ✅ **SUCCESS**

## Previous Sprint - Multi-Figure Removal ✅ **COMPLETED**

### 🗑️ **Remove Multi-Figure Support** ✅ **COMPLETED**
**Decision Made**: Remove multi-figure feature to simplify API and reduce maintenance burden

#### **Phase 1: Core Code Removal** ✅ **COMPLETED - COMMITTED TO BRANCH**
**Branch**: `remove_multi_figure_support` | **Commit**: `81dfc2e` | **Status**: Ready for Phase 2

- [X] **Remove Multi-Figure Logic from PlotConfig Class** ✅ **COMPLETED**
  - Location: `src/wave_view/core/config.py`
  - ✅ Removed: `is_multi_figure` property, `figure_count` property, `get_figure_config()` method
  - ✅ Simplified: Constructor to only accept single config dictionaries (not lists)
  - ✅ Updated: `__repr__()` method to remove multi-figure case
  - ✅ Ensured: Single-figure logic remains intact

- [X] **Remove Multi-Figure Test Cases** ✅ **COMPLETED**
  - Location: `tests/unit_tests/config/test_config_basic.py`, `test_config_validation.py`
  - ✅ Removed: All multi-figure test cases and helper functions
  - ✅ Updated: Error message validation tests for list rejection
  - ✅ Ensured: Tests validate that multi-figure configs are properly rejected
  - ✅ Results: 41 config tests now passing

- [X] **Update PlotConfig Factory Functions** ✅ **COMPLETED**
  - Location: `src/wave_view/api.py`
  - ✅ Updated: `config_from_yaml()` and `config_from_file()` to reject YAML lists
  - ✅ Added: Clear error messages for multi-figure rejection with migration guidance
  - ✅ Ensured: Backward compatibility for single-figure YAML files

#### **Phase 1.5: Fix Critical Blocker** ✅ **COMPLETED**
- [X] **Update SpicePlotter to Remove get_figure_config() Calls** ✅ **COMPLETED**
  - Location: `src/wave_view/core/plotter.py` line 121 - Fixed
  - Solution: Updated `create_figure()` to access `config.config` directly for single-figure support
  - Impact: All 31 failing tests now passing, plotter functionality restored
  - Additional: Fixed all related config tests and migration tests
  - Result: 220 passing, 0 failing tests (was 189 passing, 31 failing)

#### **Phase 2: Documentation & Example Updates** ✅ **COMPLETED**
- [X] **Update Documentation and Examples** ✅ **COMPLETED**
  - Location: `examples/demo_ring_osc.py`, `docs/`, `README.md`, `demo.ipynb` - All updated
  - Removed: All multi-figure configuration examples and feature references
  - Added: Examples showing separate plot() calls as recommended approach  
  - Updated: API documentation to reflect single-figure-only support
  - Updated: CHANGELOG.md with breaking change documentation

- [X] **Update Error Messages** ✅ **COMPLETED**
  - Location: Throughout codebase - All updated in Phase 1.5
  - Replaced: Multi-figure references with single-figure guidance
  - Added: Helpful migration suggestions in error messages
  - Ensure: User-friendly messaging about the change

#### **Phase 3: Final Cleanup & Validation** ✅ **COMPLETED**
- [X] **Run Complete Test Suite** ✅ **COMPLETED**
  - ✅ Verified: All 220 tests passing after multi-figure removal
  - ✅ Fixed: Integration test to use `config_from_file()` instead of removed properties  
  - ✅ Cleaned: Updated test helper docstring, removed obsolete validation tests
  - ✅ Confirmed: No remaining references to removed methods (comprehensive search completed)
  - ✅ Validated: Error messages are helpful and accurate with migration guidance

## Test Status Summary 
- **All Tests**: ✅ 220 passing, 0 failing (100% pass rate)
- **Coverage**: 91% overall with comprehensive test coverage
- **Multi-Figure Removal**: ✅ COMPLETE - All phases successfully implemented

## Git Status
- **Current Branch**: `remove_multi_figure_support` 
- **Latest Commit**: `3efeb71` - Phase 3 final cleanup and validation completed
- **Working Directory**: Clean (all phases committed)
- **Status**: ✅ Multi-figure removal COMPLETE - Branch ready for merge
  - ✅ All phases completed successfully
  - ✅ All 220 tests passing with 91% coverage
  - ✅ Clean migration path with helpful error messages

- [ ] **Update Version and CHANGELOG**
  - Bump: Version number for breaking change
  - Document: Multi-figure removal in CHANGELOG.md
  - Note: Migration guide for existing users
  - Mark: As breaking change in semantic versioning

### 🎨 **UI Polish Tasks** (HIGH PRIORITY)
- [ ] **Add Option to Disable Zoom Buttons**
  - Add configuration option to hide/disable the zoom buttons at the top of the graph
  - Should be configurable per plot or globally in plot configuration
  - Default behavior should remain unchanged (buttons visible)

- [ ] **Fix Zoom XY Button Functionality**
  - The "Zoom XY" button doesn't properly shift to zoom xy mode
  - Need to investigate plotly zoom mode configuration
  - Ensure proper toggling between pan, zoom x, zoom y, and zoom xy modes

- [ ] **Center-Align Plot Titles**
  - Plot titles should be center-justified across all plot types
  - Verify alignment works consistently across different plot configurations
  - Test with both single and multi-axis plots

## Backlog - Code Quality & Polish

### 🚀 **Feature Completion** (Medium Priority)

- [ ] **Enhanced Error Messages**
  - Location: `src/wave_view/core/reader.py:97-101`
  - Add fuzzy matching suggestions for signal name typos
  - Improve user experience with helpful error guidance

### 📦 **Release Preparation** (Medium Priority)
- [ ] **PyPI Publication** (Ready when multi-figure removal is complete)
  - Package has been tested and is functionally complete
  - Multi-figure removal will be a breaking change requiring version bump
  - Documentation is comprehensive and up-to-date
  - Consider beta release for testing the breaking changes

### 📚 **Documentation Enhancement** (Low Priority)
- [ ] **Documentation Hosting Setup**
  - Set up Read the Docs or GitHub Pages for comprehensive documentation
  - Include interactive examples and comprehensive API reference
  - Provide migration guide for multi-figure removal

### 🧪 **Testing & Quality** (Low Priority)
- [ ] **Test Coverage Analysis**
  - Current coverage is high, maintain 90%+ on core modules
  - Focus on edge cases and error handling paths
  - Add integration tests for complete workflows

### 🔧 **Performance & Optimization** (Low Priority)
- [ ] **Performance Profiling**
  - Profile memory usage with large datasets
  - Optimize data loading and signal processing for large files
  - Consider streaming for very large datasets

## Backlog - Future Enhancements

### 🔍 **Signal Exploration Enhancement**
- [ ] Add signal metadata (units, ranges, statistics) to `explore_signals()`
- [ ] Group signals by circuit blocks or hierarchy
- [ ] Add search and filtering capabilities

### 📦 **Package Publication** ✅ **READY FOR RELEASE**
- [X] Polish README.md for PyPI ✅ **COMPLETED** 
- [X] Set up GitHub Actions for CI/CD ✅ **COMPLETED**
- [ ] **Publish to PyPI** (Ready for release)
  - Package metadata updated and modernized
  - CI/CD workflows configured for automated publishing
  - Distribution files built and validated (wave_view-0.1.0.tar.gz, wave_view-0.1.0-py3-none-any.whl)
  - All prerequisites completed - ready for `twine upload dist/*` or GitHub release

### 🎨 **Advanced Features**
- [ ] Export functionality (PNG, PDF, SVG)
- [ ] Enhanced plotting themes and aesthetics
- [ ] Configuration helper functions for common patterns

## Notes
- **Current State**: ✅ **ALL TESTS PASSING** - 226 passing, 0 failing (100% pass rate)
- **API Coverage**: 87% with comprehensive validation
- **Architecture**: Clean 3-step workflow (Discovery → Configuration → Plotting)
- **Documentation**: ✅ **COMPLETE** - Professional Sphinx documentation with comprehensive guides
- **Next Focus**: Enhanced error messages and package publication preparation
- **API Changes**: Successfully implemented explicit configuration API (removed plot_batch, auto-detection) 
- **Test Coverage**: 92% overall coverage with comprehensive test suite
- **Code Quality**: ✅ **High priority code organization tasks completed** - extracted utilities, replaced magic numbers, added type annotations 