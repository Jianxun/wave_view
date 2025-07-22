import unittest
import yaml2plot as y2p
from pathlib import Path
import plotly.graph_objects as go


class TestPreloadWorkflow(unittest.TestCase):
    """User story: pre-load data once, reuse across multiple plots."""

    @classmethod
    def setUpClass(cls):
        raw_file = Path("tests/raw_files/Ring_Oscillator_7stage.raw")
        dataset = y2p.load_spice_raw(raw_file)
        cls.dataset = dataset

    def test_first_plot(self):
        spec = y2p.PlotSpec.from_yaml(
            """
            title: "Preload – VDD"
            x:
              signal: "time"
            y:
              - label: "VDD"
                signals:
                  VDD: "v(vdd)"
            """
        )
        fig = y2p.plot(self.dataset, spec, show=False)
        self.assertIsInstance(fig, go.Figure)

    def test_second_plot(self):
        spec = y2p.PlotSpec.from_yaml(
            """
            title: "Preload – BUS"
            x:
              signal: "time"
            y:
              - label: "BUS01"
                signals:
                  Bus06: "v(bus06)"
            """
        )
        fig = y2p.plot(self.dataset, spec, show=False)
        self.assertIsInstance(fig, go.Figure)


if __name__ == "__main__":
    unittest.main()
