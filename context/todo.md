# Project Todo List

## Current Sprint - Version 1.0.0 Architecture Implementation 🚀 **PHASE 1.2 COMPLETED**

### 📋 **v1.0.0 Implementation Status**

#### **Phase 1: Core API Refactoring** ✅ **COMPLETED**
- [X] **PlotSpec Simplification** ✅ **COMPLETED**
  - ✅ Remove plotting methods from PlotSpec class
  - ✅ Focus on configuration-only functionality  
  - ✅ Maintain factory methods (`from_yaml`, `from_file`)
  - ✅ Add clean `to_dict()` export method for v1.0.0 plotting functions
  - ✅ Archive v0.2.0 implementation in `src/wave_view/_archive/plotspec_v0_2_0.py`
  - ✅ Update tests using strict TDD methodology (6 tests passing, 88% coverage)
  
- [X] **Standalone Plotting Functions** ✅ **COMPLETED**
  - ✅ Create `wv.plot_v1(data: Dict[str, np.ndarray], spec: PlotSpec)` function
  - ✅ Implement helper functions: `create_figure()`, `create_layout()`, `add_waveform()`
  - ✅ Remove SpiceData dependency from plotting functions
  - ✅ Direct signal lookup without complex resolution
  - ✅ Multi-axis support with proper domain calculation
  - ✅ Full test coverage with integration tests (15 tests passing, 93% coverage)
  
- [ ] **Signal Resolution Simplification** (OPTIONAL - may be complete)
  - Review if additional simplification needed
  - The new plotting functions already use direct dictionary lookup
  - Consider if old resolution logic needs removal

#### **Phase 2: API Migration and Compatibility** (MEDIUM PRIORITY)
- [ ] **Backward Compatibility Assessment**
  - Analyze impact of replacing `wv.plot()` with `wv.plot_v1()`
  - Create migration guide for existing users
  - Consider deprecation warnings for old API

- [ ] **Data Preparation Layer** (FUTURE)
  - Create lambda-based signal processing utilities
  - Implement standalone data preparation functions
  - Design backward compatibility wrappers

#### **Phase 3: Multi-Case Foundation** (FUTURE)
- [ ] **Multi-Case Plotting Functions**
  - Implement `wv.plot_multi_case()`
  - Design PVT corner plotting
  - Create Monte Carlo visualization support

### 📋 **Phase 1.2 Accomplishments** ✅ **TDD MILESTONE ACHIEVED**

#### **Standalone Plotting Functions Success** ✅ **MAJOR ARCHITECTURAL ACHIEVEMENT**
- **Achievement**: Successfully implemented v1.0.0 plotting functions using strict TDD methodology
- **New Module**: `src/wave_view/core/plotting.py` with clean function-based API
- **Core Functions**: 
  - `plot(data: Dict[str, np.ndarray], spec: PlotSpec)` - Main plotting function
  - `create_figure()` - Empty figure creation helper
  - `create_layout()` - Layout configuration builder
  - `add_waveform()` - Trace addition utility
- **API Integration**: Exported as `wave_view.plot_v1()` for testing and transition
- **Test Coverage**: 93% coverage with comprehensive unit and integration tests

#### **Architecture Compliance** ✅ **DESIGN VALIDATION**
- **Simple Data Interface**: Pure `Dict[str, np.ndarray]` input, no complex objects
- **Direct Signal Lookup**: No complex resolution logic, simple dictionary access
- **PlotSpec Integration**: Clean use of `spec.to_dict()` for configuration export
- **Multi-Axis Excellence**: Proper domain calculation and Y-axis assignment
- **Error Handling**: Clear error messages for missing signals with available signal lists
- **Theme Support**: Full Plotly theme integration (plotly_dark, etc.)

#### **TDD Success Story - Phase 1.2** ✅ **METHODOLOGY VALIDATION**
- **Red Phase**: Created 7 failing tests for plotting functions ✅
- **Green Phase**: Implemented functions to make all tests pass ✅
- **Integration**: Added real data integration tests with Ring Oscillator SPICE data ✅
- **Results**: 15 tests passing (100% pass rate)
- **Coverage**: plotting.py 93%, PlotSpec 88%
- **Quality**: Clean separation of concerns, no coupling to old architecture

### 📋 **PlotSpec v1.0.0 Refactoring Success** ✅ **COMPLETED**
- **Achievement**: Successfully completed first major step of v1.0.0 architecture using strict TDD methodology
- **Approach**: Red → Green → Refactor cycle with immediate test verification for each change
- **Breaking Changes**: Cleanly removed plotting methods while preserving configuration functionality
- **Results**: 
  - ✅ All 6 tests passing (100% pass rate)
  - ✅ PlotSpec coverage improved from 67% to 88%
  - ✅ Configuration-only class achieved (separation of concerns)
  - ✅ Clean `to_dict()` method for v1.0.0 plotting functions
  - ✅ v0.2.0 implementation properly archived for reference

## Next Sprint - v1.0.0 Completion and Release

### 📋 **Phase 1.3: Final API Cleanup** (HIGH PRIORITY)
- [ ] **Migrate Main API Function**
  - Replace `wv.plot()` with v1.0.0 implementation
  - Add deprecation warnings for transition period
  - Update all examples and documentation

- [ ] **Remove Legacy Dependencies**
  - Evaluate if old plotter.py can be simplified or removed
  - Clean up unused SpiceData coupling in plotting logic
  - Simplify reader.py signal resolution if needed

### 📋 **Release Preparation** (HIGH PRIORITY)
- [ ] **Version Bump and Documentation**
  - Update version to 1.0.0 (breaking changes)
  - Create comprehensive migration guide
  - Update CHANGELOG.md with breaking changes
  - Update README.md with new API examples

- [ ] **Testing and Validation**
  - Run full test suite with new API
  - Test backward compatibility scenarios
  - Validate examples and documentation

### 📋 **Future Development**
- [ ] **Enhanced Features** (v1.1.0)
  - Advanced signal processing functions
  - Additional plot types and themes
  - Performance optimizations

- [ ] **Multi-Case Support** (v1.2.0)
  - PVT corner analysis
  - Monte Carlo visualization
  - Parameter sweep plotting

## Current Branch Status
- **Branch**: `1.0.0`
- **Working Directory**: Ready for commit
- **Test Status**: All v1.0.0 tests passing (15/15)
- **Coverage**: plotting.py 93%, PlotSpec 88%
- **Files Ready for Commit**:
  - `src/wave_view/core/plotting.py` - New v1.0.0 plotting functions
  - `tests/unit_tests/test_plotting_v1_0_0.py` - Comprehensive unit tests
  - `tests/test_integration_v1_0_0.py` - Integration tests with real data
  - `src/wave_view/__init__.py` - Added plot_v1 export
  - Updated context files

## Notes
- **Current State**: v1.0.0 Phase 1.2 successfully completed using TDD methodology
- **Architecture**: Clean function-based API with separation of concerns
- **Next Focus**: Complete Phase 1.3 and prepare for v1.0.0 release
- **Major Achievement**: 93% test coverage with comprehensive integration tests 