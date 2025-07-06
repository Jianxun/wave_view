"""
Configuration management for Wave View plotting.

This module provides the PlotConfig class for loading, validating, and managing
YAML configuration files for SPICE waveform plotting.
"""

from typing import Union, Dict, List, Any, Optional
import yaml
import os
from pathlib import Path


class PlotConfig:
    """
    Manages plot configuration from YAML files or dictionaries.
    
    Provides validation and helpful error messages for common configuration issues.
    """
    
    def __init__(self, config_source: Union[Dict, Path]):
        """
        Initialize PlotConfig from a file path or configuration data.
        
        This constructor is typically called by the config factory functions
        (config_from_file, config_from_yaml, config_from_dict) rather than directly.
        
        Args:
            config_source: Path object to YAML file or configuration dictionary
            
        Raises:
            FileNotFoundError: If config file doesn't exist
            yaml.YAMLError: If YAML content is invalid
            ValueError: If configuration format is invalid
        """
        self._config_source = config_source
        self._config_dir = None
        
        if isinstance(config_source, Path):
            # Load from file
            config_path = config_source
            self._config_dir = config_path.parent
            
            if not config_path.exists():
                raise FileNotFoundError(f"Configuration file not found: {config_path}")
            
            try:
                with open(config_path, 'r') as f:
                    loaded_config = yaml.safe_load(f)
            except yaml.YAMLError as e:
                raise yaml.YAMLError(f"Invalid YAML in config file '{config_path}': {e}")
            
            # Reject multi-figure configurations (YAML lists)
            if isinstance(loaded_config, list):
                raise ValueError(
                    f"Multi-figure configurations are no longer supported. "
                    f"The configuration file '{config_path}' contains a list of figures. "
                    f"Please create separate configuration files for each figure and "
                    f"call plot() multiple times instead."
                )
            
            self._config = loaded_config
                
        elif isinstance(config_source, dict):
            # Use dictionary directly
            self._config = config_source.copy()
        elif isinstance(config_source, list):
            # Explicitly reject lists
            raise ValueError(
                "Multi-figure configurations are no longer supported. "
                "Please create separate PlotConfig objects for each figure and "
                "call plot() multiple times instead."
            )
        else:
            raise ValueError(f"Config source must be Path or dict, got {type(config_source)}")
        
        # Validate basic structure
        self._validate_basic_structure()
    

    
    def _validate_basic_structure(self):
        """Validate basic configuration structure."""
        if not isinstance(self._config, dict):
            raise ValueError("Configuration must be a dictionary")
    

    
    @property
    def config(self) -> Dict[str, Any]:
        """Get the raw configuration dictionary."""
        return self._config
    
    def get_raw_file_path(self) -> Optional[str]:
        """
        Get the raw file path, resolving relative paths if needed.
        
        Returns:
            Absolute path to raw file, or None if not specified
        """
        source = self._config.get("source")
        if not source:
            return None
        
        # If we have a config directory and source is relative, make it absolute
        if self._config_dir and not os.path.isabs(source):
            return str(self._config_dir / source)
        
        return source
    
    def validate(self, spice_data=None) -> List[str]:
        """
        Validate configuration against optional SPICE data.
        
        Args:
            spice_data: SpiceData object to validate signals against (optional)
            
        Returns:
            List of warning messages (empty if no warnings)
        """
        warnings = []
        
        config = self._config
        
        # Check required fields
        if "X" not in config:
            warnings.append("Missing required 'X' configuration")
        elif not isinstance(config["X"], dict) or "signal_key" not in config["X"]:
            warnings.append("X configuration must have 'signal_key'")
        
        if "Y" not in config:
            warnings.append("Missing required 'Y' configuration")
        elif not isinstance(config["Y"], list):
            warnings.append("Y configuration must be a list")
        else:
            # Validate Y axis configurations
            for j, y_config in enumerate(config["Y"]):
                if not isinstance(y_config, dict):
                    warnings.append(f"Y[{j}] must be a dictionary")
                    continue
                
                if "signals" not in y_config:
                    warnings.append(f"Y[{j}] missing 'signals'")
                    continue
                
                if not isinstance(y_config["signals"], dict):
                    warnings.append(f"Y[{j}]['signals'] must be a dictionary")
        
        # Validate signals against SPICE data if provided
        if spice_data:
            warnings.extend(self._validate_signals_against_data(config, spice_data, ""))
        
        return warnings
    
    def _validate_signals_against_data(self, config: Dict, spice_data, prefix: str) -> List[str]:
        """Validate signal references against actual SPICE data."""
        warnings = []
        available_signals = set(spice_data.signals)
        
        # Check X axis signal
        x_signal = config.get("X", {}).get("signal_key", "")
        if x_signal.startswith("raw."):
            signal_name = x_signal[4:]  # Remove "raw." prefix
            if signal_name not in available_signals:
                warnings.append(f"{prefix}X signal '{signal_name}' not found in raw file")
        
        # Check Y axis signals
        for j, y_config in enumerate(config.get("Y", [])):
            for legend_name, signal_key in y_config.get("signals", {}).items():
                if signal_key.startswith("raw."):
                    signal_name = signal_key[4:]  # Remove "raw." prefix
                    if signal_name not in available_signals:
                        warnings.append(
                            f"{prefix}Y[{j}] signal '{legend_name}' -> '{signal_name}' "
                            f"not found in raw file"
                        )
                elif signal_key.startswith("data."):
                    # Data signals are processed signals - can't validate without context
                    pass
                else:
                    # Assume it's a raw signal without prefix
                    if signal_key not in available_signals:
                        warnings.append(
                            f"{prefix}Y[{j}] signal '{legend_name}' -> '{signal_key}' "
                            f"not found in raw file"
                        )
        
        return warnings
    

    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return self._config.copy()
    
    @classmethod
    def from_template(cls, template_name: str) -> 'PlotConfig':
        """
        Create configuration from a built-in template.
        
        Args:
            template_name: Name of the template
            
        Returns:
            PlotConfig instance
            
        Note:
            Template functionality to be implemented with common patterns
        """
        # TODO: Implement template system
        templates = {
            "basic": {
                "title": "Basic Waveform Plot",
                "X": {"signal_key": "raw.time", "label": "Time (s)"},
                "Y": [{
                    "label": "Voltage (V)",
                    "signals": {"Signal": "v(out)"}
                }]
            }
        }
        
        if template_name not in templates:
            available = ", ".join(templates.keys())
            raise ValueError(f"Template '{template_name}' not found. Available: {available}")
        
        return cls(templates[template_name])
    
    def __repr__(self) -> str:
        """String representation of PlotConfig."""
        title = self._config.get("title", "Untitled")
        return f"PlotConfig('{title}')" 