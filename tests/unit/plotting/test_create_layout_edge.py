import pytest

from wave_view.core.plotting import create_layout


class TestCreateLayoutEdgeCases:
    """Edge-case verification for create_layout()."""

    def test_single_axis_defaults(self):
        cfg = {
            "x": "time",
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
            "x": "time",
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
            "x": "time",
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
            "x": "time",
            "y": [
                {"label": "Voltage", "signals": {"Out": "v(out)"}},
            ],
            "show_rangeslider": False,
        }
        layout = create_layout(cfg)
        assert layout["xaxis"]["rangeslider"]["visible"] is False 