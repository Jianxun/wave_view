# Project Todo List

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

## Backlog - Code Quality & Polish

### 🔧 **Code Organization & Quality** (High Priority)
- [ ] **Extract Signal Categorization Utility** 
  - Location: `src/wave_view/api.py:285-300` in `explore_signals()`
  - Create reusable utility function for voltage/current/other signal categorization
  - Replace hardcoded logic with clean, testable utility

- [ ] **Replace Magic Numbers with Named Constants**
  - Location: `src/wave_view/core/reader.py:95-96` 
  - Replace hardcoded `[:5]` with `MAX_SIGNALS_TO_SHOW = 5`
  - Improve code readability and maintainability

- [ ] **Add Missing Type Annotations**
  - Location: `src/wave_view/api.py:145-166`
  - Complete type hints on internal functions: `_configure_plotly_renderer()`, `_is_jupyter_environment()`
  - Ensure consistent type annotation across all functions

### 🚀 **Feature Completion** (Medium Priority)
- [X] **Complete plot_batch Grid Layout or Remove Parameter** ✅ **COMPLETED**
  - Location: `src/wave_view/api.py:456-458`
  - **RESOLUTION**: Removed plot_batch() function entirely to simplify API

- [ ] **Enhanced Error Messages**
  - Location: `src/wave_view/core/reader.py:97-101`
  - Add fuzzy matching suggestions for signal name typos
  - Improve user experience with helpful error guidance

### 📚 **Documentation Polish** (Low Priority)
- [ ] **Standardize Docstring Examples**
  - Ensure consistent documentation format across all API functions
  - Add missing examples where needed

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
- **Next Focus**: Code quality polish before publication
- **API Changes**: Successfully implemented explicit configuration API (removed plot_batch, auto-detection) 
- **Test Coverage**: 92% overall coverage with comprehensive test suite 