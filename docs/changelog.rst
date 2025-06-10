Changelog
=========

All notable changes to wave_view will be documented in this file.

Version 0.1.0 (2025-01-XX)
---------------------------

**Initial Release**

Features
~~~~~~~~

* **Core API Functions**:
  
  * ``plot()`` - Main plotting function with required configuration parameter
  * ``explore_signals()`` - Signal discovery with categorized output  
  * ``load_spice()`` - SPICE file loading with Path object support
  * ``validate_config()`` - Configuration validation with helpful warnings

* **Configuration System**:

  * ``config_from_file()`` - Load configuration from YAML files
  * ``config_from_yaml()`` - Create configuration from YAML strings  
  * ``config_from_dict()`` - Create configuration from Python dictionaries
  * Multi-figure support for complex layouts
  * Comprehensive validation with clear error messages

* **SPICE Data Handling**:

  * Case-insensitive signal access (all normalized to lowercase)
  * Automatic signal categorization (voltage, current, other)
  * Modern pathlib integration throughout API
  * Support for processed data integration

* **Advanced Plotting**:

  * Plotly-based interactive plots
  * Logarithmic scale support (both X and Y axes)
  * Customizable plot titles, labels, and styling
  * Grid and legend control
  * Multi-subplot layouts

Architecture
~~~~~~~~~~~~

* **Clean 3-Step Workflow**: Discovery → Configuration → Plotting
* **Explicit over Implicit**: No hidden magic, all behavior transparent
* **Modern src/ Layout**: Ready for PyPI publication
* **Comprehensive Test Suite**: 226 tests with 92% coverage

Dependencies
~~~~~~~~~~~~

* plotly >= 5.0.0
* numpy >= 1.20.0  
* PyYAML >= 6.0
* spicelib >= 1.0.0

Supported Python
~~~~~~~~~~~~~~~~

* Python 3.8+
* Tested on Python 3.8, 3.9, 3.10, 3.11, 3.12

Known Issues
~~~~~~~~~~~~

* None at initial release

---

**Legend**:

* 🎉 **New Features**: New functionality added
* 🐛 **Bug Fixes**: Issues resolved  
* 📝 **Documentation**: Documentation improvements
* ⚠️ **Breaking Changes**: Changes that break backward compatibility
* 🔧 **Internal**: Internal improvements not affecting public API 