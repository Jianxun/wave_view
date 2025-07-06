import unittest
import wave_view as wv
from pathlib import Path
import plotly.graph_objects as go
import tempfile

yaml_content = """
title: "YAML Spec Workflow"
x: "time"
y:
  - label: "VDD"
    signals:
      VDD: "v(vdd)"
"""


class TestYAMLSpecWorkflow(unittest.TestCase):
    """User story: load PlotSpec from YAML file and plot."""

    def test_yaml_spec_plot(self):
        raw_file = Path("tests/raw_files/Ring_Oscillator_7stage.raw")
        data, _ = wv.load_spice_raw(raw_file)

        with tempfile.NamedTemporaryFile("w", suffix=".yml", delete=False) as tmp:
            tmp.write(yaml_content)
            tmp_path = Path(tmp.name)

        try:
            spec = wv.PlotSpec.from_yaml(tmp_path.read_text())
            fig = wv.plot(data, spec, show=False)
            self.assertIsInstance(fig, go.Figure)
        finally:
            tmp_path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main() 