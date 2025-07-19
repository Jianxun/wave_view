"""
Test both intuitive and legacy scale syntax support.
"""
import pytest
from src.wave_view.core.plotting import _configure_x_axis, _create_single_y_axis_config


def test_x_axis_scale_log_syntax():
    """Test that X-axis supports both scale: log and log_scale: true."""
    # Test intuitive syntax: scale: "log"
    config_intuitive = {"x": {"signal": "frequency", "scale": "log"}}
    result = _configure_x_axis(config_intuitive)
    assert result["xaxis"]["type"] == "log"
    
    # Test legacy syntax: log_scale: true
    config_legacy = {"x": {"signal": "frequency", "log_scale": True}}
    result = _configure_x_axis(config_legacy)
    assert result["xaxis"]["type"] == "log"
    
    # Test that both together work (intuitive takes precedence)
    config_both = {"x": {"signal": "frequency", "scale": "log", "log_scale": False}}
    result = _configure_x_axis(config_both)
    assert result["xaxis"]["type"] == "log"
    
    # Test linear scale
    config_linear = {"x": {"signal": "frequency", "scale": "linear"}}
    result = _configure_x_axis(config_linear)
    assert "type" not in result["xaxis"] or result["xaxis"].get("type") != "log"


def test_y_axis_scale_log_syntax():
    """Test that Y-axis supports both scale: log and log_scale: true."""
    # Test intuitive syntax: scale: "log"
    y_spec_intuitive = {"label": "Voltage", "signals": {"V": "v(out)"}, "scale": "log"}
    result = _create_single_y_axis_config(y_spec_intuitive, [0.0, 1.0], 0, {})
    assert result["type"] == "log"
    
    # Test legacy syntax: log_scale: true
    y_spec_legacy = {"label": "Voltage", "signals": {"V": "v(out)"}, "log_scale": True}
    result = _create_single_y_axis_config(y_spec_legacy, [0.0, 1.0], 0, {})
    assert result["type"] == "log"
    
    # Test that both together work (intuitive takes precedence)
    y_spec_both = {"label": "Voltage", "signals": {"V": "v(out)"}, "scale": "log", "log_scale": False}
    result = _create_single_y_axis_config(y_spec_both, [0.0, 1.0], 0, {})
    assert result["type"] == "log"
    
    # Test linear scale
    y_spec_linear = {"label": "Voltage", "signals": {"V": "v(out)"}, "scale": "linear"}
    result = _create_single_y_axis_config(y_spec_linear, [0.0, 1.0], 0, {})
    assert "type" not in result or result.get("type") != "log"


def test_plotspec_scale_field():
    """Test that PlotSpec can handle the scale field."""
    from src.wave_view.core.plotspec import PlotSpec
    
    # Test X-axis with scale field
    spec_dict = {
        "title": "Test Plot",
        "x": {"signal": "frequency", "scale": "log"},
        "y": [{"label": "Voltage", "signals": {"V": "v(out)"}}]
    }
    
    spec = PlotSpec.model_validate(spec_dict)
    assert spec.x.scale == "log"
    
    # Test Y-axis with scale field
    spec_dict = {
        "title": "Test Plot", 
        "x": {"signal": "frequency"},
        "y": [{"label": "Voltage", "signals": {"V": "v(out)"}, "scale": "log"}]
    }
    
    spec = PlotSpec.model_validate(spec_dict)
    assert spec.y[0].scale == "log"
    
    # Test to_dict() includes scale field
    config = spec.to_dict()
    assert config["y"][0]["scale"] == "log" 