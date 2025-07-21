import pytest
from click.testing import CliRunner
from unittest.mock import patch
from yaml2plot.cli import cli


@pytest.fixture
def runner():
    return CliRunner()


@patch("yaml2plot.cli.load_spice_raw")
def test_signals_all_option(mock_load_spice_raw, runner):
    """Test the 'signals' command with the -a/--all option."""
    # Arrange
    mock_signals = {f"v(sig{i})": [] for i in range(20)}
    mock_load_spice_raw.return_value = (mock_signals, {})

    with runner.isolated_filesystem():
        with open("dummy.raw", "w") as f:
            f.write("dummy data")

        # Act
        result = runner.invoke(cli, ["signals", "-a", "dummy.raw"])

        # Assert
        assert result.exit_code == 0
        assert "Found 20 signals" in result.output
        assert "v(sig19)" in result.output
        assert "..." not in result.output


@patch("yaml2plot.cli.load_spice_raw")
def test_signals_default_limit(mock_load_spice_raw, runner):
    """Test the 'signals' command with the default limit."""
    # Arrange
    mock_signals = {f"v(sig{i})": [] for i in range(20)}
    mock_load_spice_raw.return_value = (mock_signals, {})

    with runner.isolated_filesystem():
        with open("dummy.raw", "w") as f:
            f.write("dummy data")

        # Act
        result = runner.invoke(cli, ["signals", "dummy.raw"])

        # Assert
        assert result.exit_code == 0
        assert "Found 20 signals" in result.output
        assert "v(sig9)" in result.output
        assert "v(sig10)" not in result.output
        assert "... and 10 more signals" in result.output


@patch("yaml2plot.cli.load_spice_raw")
def test_signals_grep_option(mock_load_spice_raw, runner):
    """Test the 'signals' command with the --grep option."""
    # Arrange
    mock_signals = {"v(out)": [], "v(in)": [], "i(vdd)": []}
    mock_load_spice_raw.return_value = (mock_signals, {})

    with runner.isolated_filesystem():
        with open("dummy.raw", "w") as f:
            f.write("dummy data")

        # Act
        result = runner.invoke(cli, ["signals", "--grep", "v\\(", "dummy.raw"])

        # Assert
        assert result.exit_code == 0
        assert "Found 2 signals (out of 3 total)" in result.output
        assert "v(out)" in result.output
        assert "v(in)" in result.output
        assert "i(vdd)" not in result.output
