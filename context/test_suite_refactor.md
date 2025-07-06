# Test Suite Refactor Architecture (v1.0.0)

## 1. Overview
This document captures the high-level architecture, guiding principles, and incremental plan for rebuilding the `tests/` tree so it fully aligns with the **wave_view v1.0.0** API, while embracing the philosophy of **"tests as documentation."**  It serves as a living reference across multiple development sessions.

## 2. Guiding Principles
1. **Behaviour-oriented** – tests should exercise the *public API only* and verify externally-observable behaviour (return values, generated `plotly` figures, error messages). Implementation details are *not* asserted.
2. **Narrative naming** – each test tells a concise user story; filenames and test functions read like documentation.
3. **One scenario per test** – keep individual tests focused and atomic.
4. **Minimal mocking** – treat the library as a black box except for unavoidable stubs (e.g. filesystem, Plotly renderer).
5. **Refactor resilience** – tests remain valid through internal rewrites; they fail *only* when the public contract changes.

## 3. Directory Structure (target state)
```
tests/
  workflows/                # High-level user workflows (documentation tests)
    test_path_plot.py       # "Plot from raw filepath" scenario
    test_preload_plot.py    # "Pre-load data, reuse across plots" scenario
    test_yaml_spec_plot.py  # "YAML spec file → Figure" scenario
    test_cli_plot.py        # CLI smoke test via subprocess

  unit/                     # Focused unit tests for new core modules
    test_wavedataset.py
    test_plotting_layout.py
    test_plotting_axes.py
    ...

  fixtures/                 # Small RAW files & YAML specs for tests
    Ring_Oscillator_7stage.raw
    minimal_spec.yml

  _legacy/                  # Archived pre-v1.0.0 tests (ignored by pytest)
```

*Any test importing `SpiceData`, `SpicePlotter`, or calling `load_spice()` is moved to `_legacy/` and excluded from collection & coverage.*

## 4. Incremental Refactor Phases
| Phase | Goal | Key Tasks |
|-------|------|-----------|
| **A – Clean slate** | Ensure test discovery succeeds with no failing legacy tests | 1. Create branch `test_suite_refactor`  2. Move/delete legacy test folders  3. Update `pytest.ini` to ignore `_legacy/` |
| **B – Documentation workflows** | Add 4 high-level tests under `workflows/` | – Use small Ring-Osc fixture  – Assert figure creation, trace count, layout title, etc. |
| **C – Unit coverage** | Re-establish fine-grained tests for new modules | – Port critical assertions from old suite  – Focus on `core.plotting` & `core.wavedataset`  – Keep tests short & behaviour-focused |
| **D – Coverage & CI** | Polish for release readiness | – Target ≥ 85 % overall coverage  – Add coverage gate to CI  – Decide whether to delete `_legacy/` outright |

## 5. Coverage & CI Targets
* **Overall coverage**: ≥ 85 %
* **`core.plotting` coverage**: ≥ 90 %
* CI pipeline will fail if coverage drops below threshold or if any test under `tests/workflows/` fails.

## 6. Future Considerations
* Add new workflow tests whenever user-facing behaviour is added (e.g. complex-number handling, corner plotting).  These act both as regression tests and living documentation.
* Legacy tests can be fully removed once confidence in new suite is established.
* Consider generating HTML docs from workflow test docstrings for user guides.

## Stage C – Unit Coverage Rebuild Plan (v1.0.0)

### 1. Directory Layout
```
tests/
  unit/
    plotting/          # algorithm helpers (layout, domains…)
    wavedataset/       # IO & data-lookup behaviour
    plotspec/          # validation & YAML round-trip
    fixtures/          # tiny raw/YAML snippets (if needed)
```

### 2. Coverage Targets
| Module | Target |
|--------|--------|
| `core.plotting`   | ≥ 90 % |
| `core.wavedataset`| ≥ 95 % |
| `core.plotspec`   | ≥ 85 % |

### 3. Naming & Style
* Filenames: `test_<feature>_<behaviour>.py`
* One narrative assertion per test – black-box behaviour only.

### 4. Fixtures & Mocking
* Tiny NumPy arrays for plotting cases.
* Patch `WaveDataset.RawRead` to avoid file IO.
* `show=False` everywhere; no renderer side-effects.

### 5. Incremental TDD Roadmap
1. **plotting**
   * `_calculate_y_axis_domains()` single vs multi.
   * `_config_zoom()` flag logic.
   * `add_waveform()` y-axis assignment.
   * `create_layout()` happy path & edge cases.
2. **wavedataset**
   * `signals` normalisation.
   * `get_signal()` ndarray & case-insensitive.
   * `has_signal()` truth table.
   * `from_raw()` validation errors.
3. **plotspec**
   * `from_yaml()` parse.
   * `to_dict()` round-trip.
   * invalid YAML raises error.
   * override precedence via `_apply_overrides()`.

### 6. Cleanup Tasks
* Delete legacy `tests/unit_tests/*` once parity met.
* Remove zoom-button skips when legacy files archived.

### 7. Milestones / PR Slices
1. plotting helper tests (get plotting coverage to 90 %).
2. wavedataset suite.
3. plotspec suite.
4. remove old unit_tests tree & adjust `pytest.ini`.
5. add coverage gate in CI. 