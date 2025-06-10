# Project Todo List

## Current Sprint - Documentation Configuration Update ✅ **COMPLETED**

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

## Backlog - Code Quality & Polish

### 🚀 **Feature Completion** (Medium Priority)
- [X] **Complete plot_batch Grid Layout or Remove Parameter** ✅ **COMPLETED**
  - Location: `src/wave_view/api.py:456-458`
  - **RESOLUTION**: Removed plot_batch() function entirely to simplify API

- [ ] **Enhanced Error Messages**
  - Location: `src/wave_view/core/reader.py:97-101`
  - Add fuzzy matching suggestions for signal name typos
  - Improve user experience with helpful error guidance

### 📚 **Documentation Polish** (Low Priority)
- [X] **Create Comprehensive Sphinx Documentation** ✅ **COMPLETED**
  - Complete documentation structure with user guides and API reference
  - Professional Read the Docs theme with proper navigation
  - Examples, configuration guide, and contributing guidelines
  - Ready for publication and user onboarding

## Backlog - Future Enhancements

### 🔍 **Signal Exploration Enhancement**
- [ ] Add signal metadata (units, ranges, statistics) to `explore_signals()`
- [ ] Group signals by circuit blocks or hierarchy
- [ ] Add search and filtering capabilities

### 📦 **Package Publication**
- [ ] Polish README.md for PyPI
- [ ] Set up GitHub Actions for CI/CD
- [ ] Publish to PyPI (python -m build, twine upload)

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