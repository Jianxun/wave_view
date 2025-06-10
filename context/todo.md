# Project Todo List

## Current Sprint - Fix Broken Tests (URGENT)

### 🚨 **Test Failures from API Changes** (HIGH PRIORITY)
- [ ] **Fix PlotConfig Constructor Tests** (11 tests failing)
  - Update tests in `test_config_basic.py` (8 tests), `test_basic.py` (2 tests), `test_config_features.py` (3 tests)
  - Replace string parameter tests with explicit config_from_file() calls
  - Remove tests for removed auto-detection functionality

- [ ] **Fix plot() Function API Tests** (4 tests failing)
  - Update `test_api_plot.py` (2 tests) and `test_path_support.py` (2 tests)
  - Replace file path parameters with config_from_file() usage
  - Update mock expectations to match new PlotConfig object behavior

- [ ] **Remove plot_batch Tests** (8 tests failing)
  - Delete or disable `test_plot_batch.py` entirely
  - Function was removed from API for simplification
  - Update any integration tests that referenced plot_batch()

- [ ] **Fix Internal Method Tests** (4 tests failing)
  - Remove TestFilePathDetection class from `test_config_basic.py`
  - `_looks_like_file_path()` method was removed with auto-detection logic
  - Clean up tests that relied on internal implementation details

- [ ] **Fix Type Import Issues** (1 test failing)
  - Fix isinstance() call in `test_path_support.py::test_all_functions_accept_path_objects`
  - Resolve PlotConfig import/typing issue in api.py
  - Ensure proper type checking across API

### 📊 **Test Status**: 207 passing, 23 failing (90% pass rate)

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
- **Current State**: ⚠️ **BREAKING CHANGES** - 207 passing, 23 failing due to API refactor
- **API Coverage**: 85% with comprehensive validation
- **Architecture**: Clean 3-step workflow (Discovery → Configuration → Plotting)
- **Next Focus**: Fix broken tests, then code quality polish before publication
- **API Changes**: Implemented explicit configuration API (removed plot_batch, auto-detection) 