# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Development Environment Setup
```bash
# Install package in development mode
make dev
# Or: pip install -e ".[dev,docs]"

# Install package only
make install
# Or: pip install -e .
```

### Testing
```bash
# Run all tests with coverage
make test
# Or: pytest --cov=wave_view --cov-report=html --cov-report=term

# Run specific test file
pytest tests/workflows/test_cli_plot.py -v

# Run tests with verbose output
pytest -v
```

### Code Quality
```bash
# Format code with Black
black src/ tests/

# Check type hints with MyPy
mypy src/wave_view

# Lint with flake8
flake8 src/ tests/

# Sort imports with isort
isort src/ tests/
```

### Documentation
```bash
# Build documentation
make docs
# Or: cd docs && make html

# Build and serve documentation locally (opens browser on port 8000)
make docs-serve
```

### Cleaning
```bash
# Clean build artifacts and cache files
make clean
```

## Architecture

Wave View is a Python package for visualizing SPICE simulation waveforms with a focus on Jupyter notebook integration. The architecture follows a modular design:

### Core Components

**Data Loading Layer (`loader.py`, `core/wavedataset.py`)**:
- `load_spice_raw()` - Main API function for loading .raw files into numpy arrays
- `WaveDataset` - Low-level data container with signal access and metadata
- Uses `spicelib` for parsing SPICE .raw files

**Configuration Layer (`core/plotspec.py`)**:
- `PlotSpec` - Pydantic-based configuration model for plot specifications
- Supports YAML configuration files for declarative plotting
- Handles multi-axis plots, signal mapping, and styling options

**Plotting Layer (`core/plotting.py`)**:
- `plot()` - Main plotting function that creates Plotly figures
- Layout management for multi-axis plots with proper scaling
- Automatic environment detection (Jupyter vs standalone Python)

**CLI Interface (`cli.py`)**:
- `waveview` command-line tool with subcommands:
  - `init` - Generate YAML plot specs from .raw files
  - `signals` - List and filter available signals
  - `plot` - Create plots from YAML specs

**Utilities (`utils/`)**:
- `env.py` - Plotly renderer auto-detection for different environments

### API Design Patterns

The package provides two main workflows:

1. **CLI-First**: Fast plotting via command line with YAML configuration
2. **Python API**: Programmatic access with full numpy array manipulation

Key design principles:
- Simple API with sensible defaults (`plot(data, spec)`)
- Declarative configuration via YAML files
- Direct numpy array access for custom signal processing
- Automatic environment detection for optimal rendering

### Project Structure
```
src/wave_view/
├── __init__.py          # Public API exports
├── cli.py               # Command-line interface
├── loader.py            # High-level data loading
├── core/
│   ├── plotspec.py      # Configuration model
│   ├── plotting.py      # Plot generation
│   └── wavedataset.py   # Low-level data handling
└── utils/
    └── env.py           # Environment detection
```

### Configuration Files

- **pyproject.toml**: Primary configuration with dependencies, development tools, and build settings
- **Makefile**: Development convenience commands
- **.cursor/rules/**: Development guidelines and workflow documentation

### Testing Strategy

Tests are organized by component type:
- `tests/unit/`: Component-specific unit tests
- `tests/workflows/`: End-to-end workflow tests
- Uses pytest with coverage reporting
- Test data stored in `tests/raw_files/`

The project follows test-driven development with incremental testing of individual features.

## Cross-Session Context Management

This project implements a comprehensive system for maintaining continuity across multiple Claude Code sessions.

### Context Files (Always Read First!)

**Essential files to read when starting a new session:**

1. **`context/memory.md`** - Project state and history
   - Current architecture status and version information
   - Recent achievements and milestones
   - Key decisions and breaking changes
   - Development branch status

2. **`context/todo.md`** - Task tracking and planning
   - Current sprint priorities
   - Backlog items with clear descriptions
   - Completed tasks for reference

3. **`CLAUDE.md`** (this file) - Development commands and architecture

### Session Workflow

#### Starting a New Session
```bash
# 1. Understand current state
cat context/memory.md context/todo.md

# 2. Check git status
git branch && git status && git log --oneline -5

# 3. Review development environment
cat CLAUDE.md  # Commands and architecture overview

# 4. Plan session focus based on current todos
```

#### During Development
- Use the TodoWrite tool to track progress within the session
- Follow test-driven development practices
- Make frequent, atomic commits with descriptive messages
- Focus on one feature/task type per branch

#### Ending a Session
```bash
# 1. Update context with progress
# Edit context/memory.md to add recent work
# Edit context/todo.md to mark completed tasks

# 2. Commit all changes
git add . && git commit -m "descriptive message"

# 3. Leave clean state for next session
git status  # Should be clean
```

### Development Guidelines

Based on `.cursor/rules/development-guidelines.mdc`:

#### Branch Management
- **Single Purpose**: Each branch has one clear focus (features OR tests OR docs)
- **Descriptive Names**: `feature_name`, `test_suite_development`, `docs_update_description`
- **Clean History**: Keep commits focused and organized

#### Task Management
- **Context Files**: Update `context/memory.md` and `context/todo.md` at session end
- **Progressive Development**: Build features incrementally
- **Test-First**: Create tests before implementing features when possible

#### Quality Standards
- All tests must pass before committing
- Run `make test` to verify full test suite
- Use code quality tools: `black`, `mypy`, `flake8`, `isort`

### Current Project Status

**Version**: 1.1.1  
**Architecture**: v1.0.0 modern API (fully implemented)  
**Test Coverage**: 61 tests passing with good coverage  
**Recent Branch**: `housekeeping-cleanup` (consolidated configurations and refactored PlotSpec.to_dict())

**Next Priorities** (check `context/todo.md` for current sprint):
- Documentation updates for v1.1.0
- Final testing and release preparation
- Advanced features in backlog

### Key Commands for Quick Start
```bash
# Set up development environment
make dev

# Run tests to verify everything works
make test

# Check current priorities
cat context/todo.md
```