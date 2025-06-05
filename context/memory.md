# Project Memory

## Project Overview
Wave View is a Python package for visualizing SPICE simulation waveforms, designed primarily for Jupyter notebook integration with Plotly-based interactive plotting.

## Current State
**✅ SPRINT 1 COMPLETE + REPO REORGANIZATION COMPLETE**
- Core wave_view package fully implemented and tested ✅
- Repository reorganized for PyPI publication ✅
- Modern Python packaging structure (src/ layout) ✅
- All tests passing (18/18) ✅
- Package installable via pip install -e . ✅

**Repository Structure:**
```
wave_view/
├── src/wave_view/           # Main package (src layout)
├── tests/                   # Consolidated test suite
├── examples/                # Demo scripts & notebooks
│   ├── data/               # Demo SPICE files
│   ├── scripts/            # Python demo scripts  
│   └── notebooks/          # Jupyter demos
├── docs/                   # Documentation
├── pyproject.toml          # Modern packaging config
├── LICENSE                 # MIT license
├── requirements-dev.txt    # Development dependencies
└── README.md              # Project documentation
```

## Key Decisions
- **Package Name**: `wave_view` (snake_case) following PEP 8 conventions
- **Structure**: src/ layout for professional Python packaging  
- **License**: MIT License for open source distribution
- **Build System**: setuptools with pyproject.toml (modern standard)
- **API Design**: Simple plot() function + advanced SpicePlotter class
- **Configuration**: YAML-based plotting configuration system
- **Case Handling**: Case-insensitive signal name matching

## Completed Features
**Core API:**
- `load_spice()` - Load SPICE files
- `plot()` - Simple plotting interface  
- `SpicePlotter` - Advanced plotting class
- `PlotConfig` - YAML configuration system
- `create_config_template()` - Auto-generate configs

**Key Capabilities:**
- Multi-figure plotting support
- Case-insensitive signal access
- Processed signal generation (lambda functions)
- YAML configuration validation
- Auto-configuration from SPICE files
- Plotly integration with Jupyter widgets

## Open Questions
None - package is ready for publication!

## Next Steps
- Polish documentation for PyPI
- Consider GitHub Actions for CI/CD
- Plan Sprint 2 features (signal exploration UI) 