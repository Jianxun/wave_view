# Wave View: A Python Toolkit for SPICE Simulation Waveform Visualization


[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

Wave View is a lightweight yet powerful Python toolkit that transforms raw SPICE ``.raw`` files into beautiful, interactive Plotly figures with minimal code.  It reads simulation traces straight into a plain ``{signal_name: np.ndarray}`` dictionary, lets you define multi-axis plots declaratively via YAML (or override them on the command line), and automatically selects the best renderer whether you are in a Jupyter notebook, VS Code, or a headless CI job.  Case-insensitive signal lookup, engineering-notation tick labels, and first-class multi-strip support help you focus on circuit analysis rather than plotting boilerplate.

![Demo](https://raw.githubusercontent.com/Jianxun/wave_view/main/examples/screenshots/wave_view_demo.png)

## Features

- **Interactive Plotly Visualization**: Modern, web-based plots with zoom, pan, and hover
- **YAML Configuration**: Flexible, reusable plotting configurations
- **Simple API**: Plot waveforms with a single function call
- **Command Line Interface**: Quick plotting from terminal with `waveview plot`
- **Automatic Environment Detection**: Auto-detection and inline plotting for Jupyter Notebooks, render in browser when running in standalone Python scripts.



## Quick Start

### Installation
```bash
pip install wave_view
```

Wave View provides two common workflows for visualizing your SPICE simulations:

* **Option A: CLI-First** – The fastest way to get from a ``.raw`` file to an interactive plot. Perfect for quick, one-off visualizations.
* **Option B: Python API** – The most flexible approach. Ideal for scripting, custom data processing, and embedding plots in notebooks or reports.


### Option A: CLI-First Workflow

Get from a raw file to a plot in three steps using the ``waveview`` command-line tool.

**Step 1: Generate a Plot Specification**

Use ``waveview init`` to create a template ``spec.yaml`` file from your simulation output. It automatically populates the file with the independent variable (like "time") and a few available signals.

```bash
waveview init your_simulation.raw > spec.yaml
```

**Step 2: Discover Signals**

Find the exact names of the signals you want to plot with ``waveview signals``.

```bash
# List the first 10 signals
waveview signals your_simulation.raw

# List all signals
waveview signals your_simulation.raw --all

# Filter signals using a regular expression
waveview signals your_simulation.raw --grep "clk"
```

**Step 3: Plot**

Edit your ``spec.yaml`` to include the signals you discovered, then use ``waveview plot`` to generate an interactive HTML file or display the plot directly.

```bash
# This command will open a browser window with your plot
waveview plot spec.yaml

# To save the plot to a file instead
waveview plot spec.yaml --output my_plot.html
```

This approach is fast, requires no Python code, and keeps your plot configuration version-controlled alongside your simulation files.

### Option B: Python API Workflow

For more advanced use cases, the Python API provides full control over data loading, processing, and plotting. This is ideal for Jupyter notebooks, custom analysis scripts, and automated report generation.

The API follows a clear three-step workflow:

1. **Data Loading** – Load the raw ``.raw`` file with ``wave_view.load_spice_raw``.
2. **Configuration** – Describe what you want to see using ``wave_view.PlotSpec``.
3. **Plotting** – Call ``wave_view.plot`` to get a Plotly figure.

**Minimal Example**

```python
import wave_view as wv

# 1. Load data from a .raw file
data, _ = wv.load_spice_raw("your_simulation.raw")
print(f"Signals available: {list(data.keys())[:5]}...")

# 2. Configure the plot using a YAML string
spec = wv.PlotSpec.from_yaml("""
title: "My Simulation Results"
x:
  signal: "time"
  label: "Time (s)"
y:
  - label: "Voltage (V)"
    signals:
      Output: "v(out)"
      Input:  "v(in)"
""")

# 3. Create and display the plot
fig = wv.plot(data, spec)
fig.show()
```

**Advanced Example: Plotting Derived Signals**

Because the API gives you direct access to the data as NumPy arrays, you can easily perform calculations and plot the results.

```python
import numpy as np
import wave_view as wv

# Load the data
data, _ = wv.load_spice_raw("your_simulation.raw")

# Calculate a new, derived signal
data["diff_voltage"] = data["v(out_p)"] - data["v(out_n)"]

# Create a spec that plots both raw and derived signals
spec = wv.PlotSpec.from_yaml("""
title: "Differential Output Voltage"
x:
  signal: "time"
  label: "Time (s)"
y:
  - label: "Voltage (V)"
    signals:
      VOUT_P: "v(out_p)"
      VOUT_N: "v(out_n)"
      VOUT_DIFF: "diff_voltage"
""")

# Create and display the plot
fig = wv.plot(data, spec)
fig.show()
```

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/Jianxun/wave_view.git
cd wave_view

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode with all dependencies
pip install -e .
pip install -r requirements-dev.txt

# Verify development setup
python -c "import wave_view as wv; print('Development setup complete!')"
```

### Run Tests

```bash
# Run all tests
pytest

# With coverage
pytest --cov=wave_view --cov-report=html

# Run specific test file
pytest tests/workflows/test_cli_plot.py -v
```

## Project Structure

```
wave_view/
├── src/wave_view/
│   ├── core/
│   │   ├── plotspec.py      # PlotSpec model
│   │   ├── plotting.py      # Plotting helpers + plot()
│   │   └── wavedataset.py   # WaveDataset + low-level loaders
│   ├── loader.py            # load_spice_raw convenience wrapper
│   ├── cli.py               # Command-line interface
│   └── __init__.py          # Public symbols (plot, PlotSpec, load_spice_raw,...)
├── tests/                   # Test suite
├── examples/                # Usage examples
├── docs/                    # Documentation
└── pyproject.toml           # Packaging
```

## Requirements

- **Python**: 3.8+
- **Core Dependencies**:
  - `plotly` >= 5.0.0 (Interactive plotting)
  - `numpy` >= 1.20.0 (Numerical operations)
  - `PyYAML` >= 6.0 (Configuration files)
  - `spicelib` >= 1.0.0 (SPICE file reading)
  - `click` >= 8.0.0 (Command line interface)

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`pytest`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Documentation

Comprehensive documentation is available with:

- **User Guides**: Installation, quickstart, and configuration
- **API Reference**: Complete function documentation
- **Examples**: Practical use cases and tutorials
- **Development**: Contributing guidelines and setup

### Build Documentation Locally

```bash
# Install documentation dependencies
pip install -e ".[docs]"

# Build documentation
make docs

# Serve documentation locally
make docs-serve  # Opens at http://localhost:8000
```

## Links

- **Documentation**: [Local Build Available]
- **PyPI Package**: [Coming Soon]  
- **Issue Tracker**: [GitHub Issues](https://github.com/Jianxun/wave_view/issues)
- **Changelog**: [CHANGELOG.md](CHANGELOG.md)

## Version

Current version: **0.1.0** (Alpha)

---

**Wave View** - Making SPICE waveform visualization simple and interactive! 🌊📈 
