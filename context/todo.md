# Project Todo List

## Current Sprint - Code Quality & Polish

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
- [ ] **Complete plot_batch Grid Layout or Remove Parameter**
  - Location: `src/wave_view/api.py:456-458`
  - Either implement grid layout functionality or remove unused `layout` parameter
  - Clean up TODO comment and unimplemented feature

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
- **Current State**: All 236 tests passing, 92% coverage overall
- **API Coverage**: 88% with comprehensive validation
- **Architecture**: Clean 3-step workflow (Discovery → Configuration → Plotting)
- **Next Focus**: Code quality polish before publication 