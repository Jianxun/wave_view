"""
Pydantic-based plot specification models.

This module provides PlotSpec and YAxisSpec classes that replace PlotConfig
with structured validation and type safety.
"""

from typing import List, Optional, Dict, Any, Union
from pathlib import Path
import yaml
import numpy as np
from pydantic import BaseModel, Field, ConfigDict
import plotly.graph_objects as go


class XAxisSpec(BaseModel):
    """X-axis configuration specification."""

    signal: str = Field(..., description="X-axis signal key")
    label: Optional[str] = Field(None, description="X-axis label")
    scale: Optional[str] = Field(None, description="Scale type: 'log' or 'linear'")
    unit: Optional[str] = Field(None, description="Unit for display")
    range: Optional[List[float]] = Field(None, description="[min, max] range")


class YAxisSpec(BaseModel):
    """Y-axis configuration specification."""

    label: str = Field(..., description="Y-axis label")
    signals: Dict[str, str] = Field(
        ..., description="Legend name -> signal key mapping"
    )
    scale: Optional[str] = Field(None, description="Scale type: 'log' or 'linear'")
    unit: Optional[str] = Field(None, description="Unit for display")
    range: Optional[List[float]] = Field(None, description="[min, max] range")
    color: Optional[str] = Field(None, description="Axis color")


class PlotSpec(BaseModel):
    """
    Pydantic-based plot specification with fluent API.

    Replaces PlotConfig with structured validation and composable workflow.
    """

    # Core configuration
    # Accept both lowercase (preferred) and uppercase aliases for backward compatibility
    x: XAxisSpec = Field(..., description="X-axis configuration", alias="X")
    y: List[YAxisSpec] = Field(..., description="Y-axis specifications", alias="Y")
    title: Optional[str] = Field(None, description="Plot title")
    raw: Optional[str] = Field(
        None, description="Path to SPICE raw file for self-contained specs"
    )

    # Styling options
    width: Optional[int] = Field(None, description="Plot width in pixels")
    height: Optional[int] = Field(None, description="Plot height in pixels")
    theme: Optional[str] = Field("plotly", description="Plot theme")

    # Title positioning
    title_x: float = Field(
        0.5, description="Title x position (0=left, 0.5=center, 1=right)"
    )
    title_xanchor: str = Field(
        "center", description="Title anchor: left, center, right"
    )

    # Advanced options
    show_legend: bool = Field(True, description="Show legend")
    grid: bool = Field(True, description="Show grid")
    show_rangeslider: bool = Field(True, description="Show range slider below X-axis")

    # Pydantic model configuration
    model_config = ConfigDict(populate_by_name=True, extra="allow")

    # Factory methods
    @classmethod
    def from_yaml(cls, yaml_str: str) -> "PlotSpec":
        """Create PlotSpec from YAML string."""
        try:
            config_dict = yaml.safe_load(yaml_str)
            if isinstance(config_dict, list):
                raise ValueError("Multi-figure configurations not supported")
            return cls.model_validate(config_dict)
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML: {e}")

    @classmethod
    def from_file(cls, file_path: Union[str, Path]) -> "PlotSpec":
        """
        Create PlotSpec from YAML file.

        Args:
            file_path: Path to YAML configuration file

        Returns:
            PlotSpec instance

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If YAML is invalid or unsupported
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {file_path}")

        try:
            yaml_content = file_path.read_text(encoding="utf-8")
            return cls.from_yaml(yaml_content)
        except Exception as e:
            raise ValueError(f"Failed to load configuration from {file_path}: {e}")

    # Configuration export methods
    def to_dict(self) -> Dict[str, Any]:
        """
        Export clean configuration dictionary for v1.0.0 plotting functions.

        Returns:
            Dict containing clean configuration suitable for standalone plotting functions
        """
        return self.model_dump(by_alias=False)
