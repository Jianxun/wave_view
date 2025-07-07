import pytest
from pathlib import Path
from wave_view.core.plotspec import PlotSpec


class TestPlotSpecFromYaml:
    """Tests for PlotSpec.from_yaml factory."""

    VALID_YAML = """
    title: "Voltage vs Time"
    x:
      signal: "time"
    y:
      - label: "Voltage (V)"
        signals:
          Out: "v(out)"
    width: 800
    height: 400
    """

    def test_parse_valid_yaml(self):
        spec = PlotSpec.from_yaml(self.VALID_YAML)
        assert spec.title == "Voltage vs Time"
        assert spec.x.signal == "time"
        assert len(spec.y) == 1
        assert spec.y[0].label == "Voltage (V)"
        assert spec.y[0].signals == {"Out": "v(out)"}
        # Optional fields
        assert spec.width == 800
        assert spec.height == 400

    def test_invalid_yaml_raises_valueerror(self):
        bad_yaml = "title: [unbalanced braces"
        with pytest.raises(ValueError):
            PlotSpec.from_yaml(bad_yaml)

    def test_multifigure_yaml_not_supported(self):
        multi_yaml = """
        - title: "Plot 1"
          x: {signal: time}
          y:
            - label: Voltage
              signals: {Out: v(out)}
        - title: "Plot 2"
          x: {signal: freq}
          y:
            - label: Current
              signals: {In: i(in)}
        """
        with pytest.raises(ValueError):
            PlotSpec.from_yaml(multi_yaml)


class TestPlotSpecRoundTrip:
    """Verify to_dict() produces expected keys and values."""

    def test_round_trip_dict_contains_core_fields(self):
        yaml_str = """
        x:
          signal: time
        y:
          - label: Voltage
            signals:
              Out: v(out)
        """
        spec = PlotSpec.from_yaml(yaml_str)
        d = spec.to_dict()

        # Core keys must exist
        for key in ["title", "x", "y", "width", "height", "theme"]:
            assert key in d

        # YAML had no title so value should be None and preserved
        assert d["title"] is None
        assert d["x"]["signal"] == "time"
        assert isinstance(d["y"], list) and len(d["y"]) == 1
        assert d["y"][0]["label"] == "Voltage"


class TestPlotSpecFromFile:
    """Lightweight checks for the disk-loading helper."""

    def test_missing_file_raises_filenotfound(self, tmp_path):
        fpath = tmp_path / "nope.yml"
        with pytest.raises(FileNotFoundError):
            PlotSpec.from_file(fpath)

    def test_from_file_success(self, tmp_path):
        cfg_path = tmp_path / "spec.yml"
        cfg_path.write_text("x: {signal: time}\ny:\n  - label: V\n    signals: {Out: v(out)}\n")
        spec = PlotSpec.from_file(cfg_path)
        assert spec.x.signal == "time" 