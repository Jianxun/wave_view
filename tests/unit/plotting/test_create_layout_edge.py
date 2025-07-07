import pytest

from wave_view.core.plotting import create_layout


class TestCreateLayoutEdgeCases:
    """Edge-case verification for create_layout()."""

    def test_single_axis_defaults(self):
        cfg = {
            "x": {"signal": "time"},
            "y": [
                {"label": "Voltage", "signals": {"Out": "v(out)"}}
            ],
        }
        layout = create_layout(cfg)

        # X-axis basic checks
        assert layout["xaxis"]["title"] == "time"
        assert layout["xaxis"]["rangeslider"]["visible"] is True

        # Y-axis occupies full domain
        assert layout["yaxis"]["domain"] == [0, 1]
        assert layout["yaxis"]["title"] == "Voltage"

    def test_multi_axis_domain_order_and_gap(self):
        cfg = {
            "x": {"signal": "time"},
            "y": [
                {"label": "Top", "signals": {"A": "a"}},
                {"label": "Bottom", "signals": {"B": "b"}},
            ],
            "grid": False,  # disable grid globally
        }
        layout = create_layout(cfg)

        # Domains should be ordered top -> bottom with a gap in between
        top_dom = layout["yaxis"]["domain"]
        bottom_dom = layout["yaxis2"]["domain"]

        assert top_dom[1] == pytest.approx(1.0)
        # bottom axis upper bound must be below top axis lower bound (gap)
        assert bottom_dom[1] < top_dom[0]
        # grid flag propagated
        assert layout["yaxis"]["showgrid"] is False
        assert layout["yaxis2"]["showgrid"] is False

    def test_log_scale_and_range_propagation(self):
        cfg = {
            "x": {"signal": "time"},
            "y": [
                {
                    "label": "Current",
                    "signals": {"I": "i"},
                    "log_scale": True,
                    "range": [1e-3, 1e-1],
                }
            ],
        }
        layout = create_layout(cfg)
        yaxis_cfg = layout["yaxis"]
        assert yaxis_cfg["type"] == "log"
        assert yaxis_cfg["range"] == [1e-3, 1e-1]

    def test_disable_rangeslider(self):
        cfg = {
            "x": {"signal": "time"},
            "y": [
                {"label": "Voltage", "signals": {"Out": "v(out)"}},
            ],
            "show_rangeslider": False,
        }
        layout = create_layout(cfg)
        assert layout["xaxis"]["rangeslider"]["visible"] is False


class TestSIEngineeringNotationEdgeCases:
    """Tests for SI engineering notation applied to all axes."""

    def test_x_axis_always_uses_si_notation(self):
        """All X-axes should use SI engineering notation for consistent formatting."""
        config = {
            "title": "Frequency Response",
            "x": {
                "signal": "frequency",
                "label": "Frequency (Hz)",
                "log_scale": True
            },
            "y": [
                {
                    "label": "Magnitude (dB)",
                    "signals": {"Output": "v(out)"}
                }
            ]
        }
        
        layout = create_layout(config)
        
        # SI engineering notation should be enabled for all X-axes
        assert layout["xaxis"]["exponentformat"] == "SI"
        assert layout["xaxis"]["type"] == "log"
        assert layout["xaxis"]["title"] == "Frequency (Hz)"
    
    def test_time_domain_x_axis_uses_si_notation(self):
        """Time domain X-axis should also use SI engineering notation."""
        config = {
            "title": "Time Domain Analysis",
            "x": {
                "signal": "time",
                "label": "Time (s)",
                "log_scale": False
            },
            "y": [
                {
                    "label": "Voltage (V)",
                    "signals": {"Output": "v(out)"}
                }
            ]
        }
        
        layout = create_layout(config)
        
        # SI engineering notation should be enabled for all signals
        assert layout["xaxis"]["exponentformat"] == "SI"
        assert layout["xaxis"]["title"] == "Time (s)"

    def test_y_axes_use_si_notation(self):
        """All Y-axes should use SI engineering notation."""
        config = {
            "title": "Multi-Axis Analysis",
            "x": {
                "signal": "time", 
                "label": "Time (s)",
                "log_scale": False
            },
            "y": [
                {
                    "label": "Voltage (V)",
                    "signals": {"Output": "v(out)"}
                },
                {
                    "label": "Current (A)",
                    "signals": {"Input": "i(in)"}
                }
            ]
        }
        
        layout = create_layout(config)
        
        # SI engineering notation should be enabled for all Y-axes
        assert layout["yaxis"]["exponentformat"] == "SI"
        assert layout["yaxis2"]["exponentformat"] == "SI"
        assert layout["yaxis"]["title"] == "Voltage (V)"
        assert layout["yaxis2"]["title"] == "Current (A)" 