Here’s a concise review of the Sphinx documentation in `docs/`, with a spotlight on `docs/examples.rst`.

1. Overall structure  
   • `index.rst`, `installation.rst`, `configuration.rst`, `quickstart.rst`, and the API stubs build a clear narrative around the new three-step workflow (load → PlotSpec → plot).  
   • The prose generally matches the v1.0.0 architecture described in `context/memory.md`.

2. Quick Start & Configuration guides  
   • `configuration.rst` is fully aligned with the Pydantic‐based `PlotSpec` model (lower-case `x` / `y` keys, `PlotSpec.from_yaml("""...""")`, etc.).  
   • `quickstart.rst` still shows two patterns that are **not implemented in code**:  
     – Calling `wv.PlotSpec.from_yaml("config.yaml")` (should be `PlotSpec.from_file` or read the file text).  
     – Passing a raw-file path directly to `wv.plot("simulation.raw", spec)` (current `plot()` only accepts a pre-loaded `Dict[str, np.ndarray]`).

3. `docs/examples.rst` – main inaccuracies  
   a. Uses the (removed) helper `wv.config_from_yaml`; replace with `wv.PlotSpec.from_yaml` or `from_file`.  
   b. Many YAML snippets still use *capital-letter* `X:` / `Y:` sections from the legacy `PlotConfig` schema; these must be lower-case `x:` / `y:` to validate.  
   c. Several examples pass `processed_data=` to `wv.plot()`; that keyword isn’t in the current signature.  
   d. Calls like `data.get_signal_data("v(out)")` or `data.get_signal("frequency")` assume a `WaveDataset` object, but `load_spice_raw()` returns a plain dict.  
   e. “data.*” signal references in YAML (e.g. `data.power_output`) won’t resolve automatically—signals need to be inserted into the data dict under those keys before calling `plot()`.  
   f. Minor: a few label strings contain Unicode (φ, ω) that are fine for Plotly but need escaping in LaTeX render targets.

4. Other files  
   • `examples.rst` is the only page still referencing removed helpers; the rest of the docs largely follow the new API.  
   • Version strings: docs claim *wave_view* 1.0.0 but `src/wave_view/__init__.py` still contains `__version__ = "0.1.0"`—worth syncing before release.

5. Suggested next actions  
   1. Update all code blocks in `examples.rst` (and a couple in `quickstart.rst`) to:  
      – Use `PlotSpec.from_yaml`/`from_file` and lower-case keys.  
      – Build derived arrays into the data dict before plotting, instead of `processed_data=`.  
      – Replace dict-access snippets (`data["v(out)"] …`) for uniformity.  
   2. Decide whether to re-introduce a convenience wrapper that lets `wv.plot()` accept a file path (and optional processed-data dict) *or* remove that usage from docs.  
   3. Bump `__version__` to 1.0.0 in `__init__.py` and in `pyproject.toml`.  
   4. Re-run `make html` after edits to ensure the build is warning-free.

In short, the bulk of the docs are ready, but `examples.rst` (and a few Quick-Start snippets) still reference legacy helpers and old configuration syntax; fixing those will bring the documentation fully in line with the finalized v1.0.0 API.