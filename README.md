# Wave View

A prototype spice simulation waveform viewer widget for IPython notebooks.

## Overview

Wave View provides an interactive widget for visualizing and analyzing SPICE simulation waveforms directly within Jupyter/IPython notebook environments. This tool allows circuit designers and engineers to examine simulation results with familiar plotting and measurement capabilities.

## Features (Planned)

- 📊 Interactive waveform plotting
- 🔍 Zoom and pan navigation
- 📏 Measurement tools (cursors, calculations)
- 📂 Support for common SPICE output formats
- 🔄 Multiple waveform overlays
- 📤 Export functionality
- ⚡ Optimized for large datasets

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd wave_view
   ```

2. Create and activate virtual environment:
   
   **For Unix/macOS:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
   
   **For Windows:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

```python
from wave_view import WaveformViewer

# Create a new viewer instance
viewer = WaveformViewer()

# Load SPICE simulation data
viewer.load_data("simulation_results.raw")

# Add signals to plot
viewer.add_signal("vout")
viewer.add_signal("vin")

# Display the waveforms
viewer.plot()
```

## Development

This project follows test-driven development practices. Run tests with:

```bash
pytest
```

Format code with:
```bash
black src/ tests/
```

Lint code with:
```bash
flake8 src/ tests/
```

## Project Status

🚧 **Under Development** - This is a prototype project in early development phase.

Current implementation status:
- [x] Project structure setup
- [x] Basic class framework
- [ ] SPICE file parsing
- [ ] Waveform plotting
- [ ] Interactive features
- [ ] Widget integration

## Contributing

This is a prototype project. Contributions and suggestions are welcome!

## License

TBD - License to be determined. 