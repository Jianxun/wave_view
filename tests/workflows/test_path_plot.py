import unittest
import yaml2plot as wv
from pathlib import Path
import plotly.graph_objects as go


class TestPathPlotWorkflow(unittest.TestCase):
    """User story: plot from raw filepath without manual data handling."""

    def test_plot_from_filepath(self):
        raw_file = Path("tests/raw_files/Ring_Oscillator_7stage.raw")
        self.assertTrue(raw_file.exists(), f"Missing fixture {raw_file}")

        # Load data then plot (single-liner could wrap later)
        dataset = wv.load_spice_raw(raw_file)

        spec = wv.PlotSpec.from_yaml(
            """
            title: "Ring Oscillator – Path Workflow"
            x:
              signal: "time"
            y:
              - label: "VDD"
                signals:
                  Bus06: "v(bus06)"
            """
        )

        fig = wv.plot(dataset, spec, show=False)
        self.assertIsInstance(fig, go.Figure)
        self.assertEqual(len(fig.data), 1)
        self.assertEqual(fig.data[0].name, "Bus06")


if __name__ == "__main__":
    unittest.main()
