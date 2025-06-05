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
    
    Supports both single-figure and multi-figure configurations, with validation
    and helpful error messages for common configuration issues.
    """
    
    def __init__(self, config_source: Union[str, Dict, List, Path]):
        """
        Initialize PlotConfig from a file path or dictionary.
        
        Args:
            config_source: Path to YAML file, Path object, configuration dictionary, or list of configs
            
        Raises:
            FileNotFoundError: If config file doesn't exist
            yaml.YAMLError: If YAML file is invalid
            ValueError: If configuration format is invalid
        """
        self._config_source = config_source
        self._config_dir = None
        
        if isinstance(config_source, (str, Path)):
            # Load from file
            config_path = Path(config_source)
            self._config_dir = config_path.parent
            
            if not config_path.exists():
                raise FileNotFoundError(f"Configuration file not found: {config_path}")
            
            try:
                with open(config_path, 'r') as f:
                    self._config = yaml.safe_load(f)
            except yaml.YAMLError as e:
                raise yaml.YAMLError(f"Invalid YAML in config file '{config_path}': {e}")
                
        elif isinstance(config_source, (dict, list)):
            # Use dictionary or list directly
            if isinstance(config_source, list):
                self._config = [cfg.copy() if isinstance(cfg, dict) else cfg for cfg in config_source]
            else:
                self._config = config_source.copy()
        else:
            raise ValueError(f"Config source must be str, Path, dict, or list, got {type(config_source)}")
        
        # Validate basic structure
        self._validate_basic_structure()
    
    def _validate_basic_structure(self):
        """Validate basic configuration structure."""
        if isinstance(self._config, list):
            # Multi-figure configuration
            for i, fig_config in enumerate(self._config):
                if not isinstance(fig_config, dict):
                    raise ValueError(f"Figure {i} configuration must be a dictionary")
        elif isinstance(self._config, dict):
            # Single figure configuration
            pass
        else:
            raise ValueError("Configuration must be a dictionary or list of dictionaries")
    
    @property
    def is_multi_figure(self) -> bool:
        """Check if this is a multi-figure configuration."""
        return isinstance(self._config, list)
    
    @property
    def config(self) -> Dict[str, Any]:
        """Get the raw configuration dictionary."""
        return self._config
    
    def get_raw_file_path(self, figure_index: int = 0) -> Optional[str]:
        """
        Get the raw file path, resolving relative paths if needed.
        
        Args:
            figure_index: Figure index for multi-figure configs (default: 0)
            
        Returns:
            Absolute path to raw file, or None if not specified
        """
        if self.is_multi_figure:
            if figure_index >= len(self._config):
                raise IndexError(f"Figure index {figure_index} out of range")
            fig_config = self._config[figure_index]
        else:
            fig_config = self._config
        
        source = fig_config.get("source")
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
        
        configs_to_validate = [self._config] if not self.is_multi_figure else self._config
        
        for i, config in enumerate(configs_to_validate):
            figure_prefix = f"Figure {i}: " if self.is_multi_figure else ""
            
            # Check required fields
            if "X" not in config:
                warnings.append(f"{figure_prefix}Missing required 'X' configuration")
            elif not isinstance(config["X"], dict) or "signal_key" not in config["X"]:
                warnings.append(f"{figure_prefix}X configuration must have 'signal_key'")
            
            if "Y" not in config:
                warnings.append(f"{figure_prefix}Missing required 'Y' configuration")
            elif not isinstance(config["Y"], list):
                warnings.append(f"{figure_prefix}Y configuration must be a list")
            else:
                # Validate Y axis configurations
                for j, y_config in enumerate(config["Y"]):
                    if not isinstance(y_config, dict):
                        warnings.append(f"{figure_prefix}Y[{j}] must be a dictionary")
                        continue
                    
                    if "signals" not in y_config:
                        warnings.append(f"{figure_prefix}Y[{j}] missing 'signals'")
                        continue
                    
                    if not isinstance(y_config["signals"], dict):
                        warnings.append(f"{figure_prefix}Y[{j}]['signals'] must be a dictionary")
            
            # Validate signals against SPICE data if provided
            if spice_data:
                warnings.extend(self._validate_signals_against_data(config, spice_data, figure_prefix))
        
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
    
    def get_figure_config(self, index: int = 0) -> Dict[str, Any]:
        """
        Get configuration for a specific figure.
        
        Args:
            index: Figure index (0 for single-figure configs)
            
        Returns:
            Figure configuration dictionary
        """
        if self.is_multi_figure:
            if index >= len(self._config):
                raise IndexError(f"Figure index {index} out of range")
            return self._config[index]
        else:
            if index != 0:
                raise IndexError("Single-figure config only has index 0")
            return self._config
    
    @property
    def figure_count(self) -> int:
        """Get the number of figures in this configuration."""
        return len(self._config) if self.is_multi_figure else 1
    
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
        if self.is_multi_figure:
            return f"PlotConfig({self.figure_count} figures)"
        else:
            title = self._config.get("title", "Untitled")
            return f"PlotConfig('{title}')" 