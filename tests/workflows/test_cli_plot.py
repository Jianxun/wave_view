import unittest
from pathlib import Path
import tempfile

from click.testing import CliRunner

import wave_view as wv
from wave_view.cli import cli


class TestCLIPlotWorkflow(unittest.TestCase):
    """Smoke-test the ``wave_view plot`` CLI command."""

    def test_cli_plot_generates_output_file(self):
        runner = CliRunner()

        raw_file = Path("tests/raw_files/Ring_Oscillator_7stage.raw")
        self.assertTrue(raw_file.exists())

        yaml_spec = """
        title: "CLI Plot Test"
        x:
          signal: "time"
        y:
          - label: "BUS06"
            signals:
              Bus06: "v(bus06)"
        """

        with tempfile.TemporaryDirectory() as tmp_dir:
            spec_path = Path(tmp_dir) / "spec.yml"
            spec_path.write_text(yaml_spec)

            output_path = Path(tmp_dir) / "plot.html"

            result = runner.invoke(
                cli,
                [
                    "plot",
                    str(spec_path),
                    str(raw_file),
                    "--output",
                    str(output_path),
                    "--renderer",
                    "json",
                ],
            )

            # Ensure CLI exited successfully
            self.assertEqual(result.exit_code, 0, msg=result.output)
            # Output file should be created
            self.assertTrue(output_path.exists())


if __name__ == "__main__":
    unittest.main() 