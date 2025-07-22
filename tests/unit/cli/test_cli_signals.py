import pytest
import xarray as xr
import numpy as np
from click.testing import CliRunner
from unittest.mock import patch
from yaml2plot.cli import cli


@pytest.fixture
def runner():
    return CliRunner()


@patch("yaml2plot.cli.load_spice_raw")
def test_signals_all_option(mock_load_spice_raw, runner):
    """Test the 'signals' command with the -a/--all option."""
    # Arrange - Mock xarray Dataset
    data_vars = {f"v(sig{i})": (["time"], np.array([])) for i in range(20)}
    mock_dataset = xr.Dataset(
        data_vars=data_vars,
        coords={"time": np.array([])}
    )
    mock_load_spice_raw.return_value = mock_dataset

    with runner.isolated_filesystem():
        with open("dummy.raw", "w") as f:
            f.write("dummy data")

        # Act
        result = runner.invoke(cli, ["signals", "-a", "dummy.raw"])

        # Assert
        assert result.exit_code == 0
        assert "Found 21 signals" in result.output  # 20 data vars + 1 coordinate
        assert "time" in result.output
        assert "v(sig19)" in result.output
        assert "..." not in result.output


@patch("yaml2plot.cli.load_spice_raw")
def test_signals_default_limit(mock_load_spice_raw, runner):
    """Test the 'signals' command with the default limit."""
    # Arrange - Mock xarray Dataset
    data_vars = {f"v(sig{i})": (["time"], np.array([])) for i in range(20)}
    mock_dataset = xr.Dataset(
        data_vars=data_vars,
        coords={"time": np.array([])}
    )
    mock_load_spice_raw.return_value = mock_dataset

    with runner.isolated_filesystem():
        with open("dummy.raw", "w") as f:
            f.write("dummy data")

        # Act
        result = runner.invoke(cli, ["signals", "dummy.raw"])

        # Assert
        assert result.exit_code == 0
        assert "Found 21 signals" in result.output  # 20 data vars + 1 coordinate
        assert "time" in result.output
        assert "v(sig8)" in result.output  # Position 10 (last shown)
        assert "v(sig9)" not in result.output  # Position 11 (first hidden)
        assert "... and 11 more signals" in result.output


@patch("yaml2plot.cli.load_spice_raw")
def test_signals_grep_option(mock_load_spice_raw, runner):
    """Test the 'signals' command with the --grep option."""
    # Arrange - Mock xarray Dataset
    mock_dataset = xr.Dataset(
        data_vars={
            "v(out)": (["time"], np.array([])),
            "v(in)": (["time"], np.array([])),
            "i(vdd)": (["time"], np.array([]))
        },
        coords={"time": np.array([])}
    )
    mock_load_spice_raw.return_value = mock_dataset

    with runner.isolated_filesystem():
        with open("dummy.raw", "w") as f:
            f.write("dummy data")

        # Act
        result = runner.invoke(cli, ["signals", "--grep", "v\\(", "dummy.raw"])

        # Assert
        assert result.exit_code == 0
        assert "Found 2 signals (out of 4 total)" in result.output  # 3 data vars + 1 coordinate
        assert "v(out)" in result.output
        assert "v(in)" in result.output
        assert "i(vdd)" not in result.output
        assert "time" not in result.output  # time doesn't match pattern v\(
