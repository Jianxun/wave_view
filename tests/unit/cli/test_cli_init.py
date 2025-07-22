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
def test_init_command_happy_path(mock_load_spice_raw, runner):
    """Test the 'init' command with a standard raw file."""
    # Arrange - Mock xarray Dataset
    mock_dataset = xr.Dataset(
        data_vars={
            "v(out)": (["time"], np.array([])),
            "v(in)": (["time"], np.array([]))
        },
        coords={"time": np.array([])}
    )
    mock_load_spice_raw.return_value = mock_dataset

    with runner.isolated_filesystem():
        with open("dummy.raw", "w") as f:
            f.write("dummy data")

        # Act
        result = runner.invoke(cli, ["init", "dummy.raw"])

        # Assert
        assert result.exit_code == 0
        assert 'title: "Analysis of dummy.raw"' in result.output
        assert 'signal: "time"' in result.output
        assert 'v(out): "v(out)"' in result.output
        assert 'v(in): "v(in)"' in result.output
        assert "# Independent variable of the simulation" in result.output


@patch("yaml2plot.cli.load_spice_raw")
def test_init_command_2_signals(mock_load_spice_raw, runner):
    """Test the 'init' command with a raw file containing 2 signals."""
    # Arrange - Mock xarray Dataset
    mock_dataset = xr.Dataset(
        data_vars={"v(out)": (["time"], np.array([]))},
        coords={"time": np.array([])}
    )
    mock_load_spice_raw.return_value = mock_dataset

    with runner.isolated_filesystem():
        with open("dummy.raw", "w") as f:
            f.write("dummy data")

        # Act
        result = runner.invoke(cli, ["init", "dummy.raw"])

        # Assert
        assert result.exit_code == 0
        assert 'signal: "time"' in result.output
        assert 'v(out): "v(out)"' in result.output
        assert 'v(in): "v(in)"' not in result.output


@patch("yaml2plot.cli.load_spice_raw")
def test_init_command_1_signal(mock_load_spice_raw, runner):
    """Test the 'init' command with a raw file containing 1 signal."""
    # Arrange - Mock xarray Dataset with only coordinate (no data vars)
    mock_dataset = xr.Dataset(
        data_vars={},
        coords={"time": np.array([])}
    )
    mock_load_spice_raw.return_value = mock_dataset

    with runner.isolated_filesystem():
        with open("dummy.raw", "w") as f:
            f.write("dummy data")

        # Act
        result = runner.invoke(cli, ["init", "dummy.raw"])

        # Assert
        assert result.exit_code == 0
        assert 'signal: "time"' in result.output
        assert "signals: {}" in result.output


@patch("yaml2plot.cli.load_spice_raw")
def test_init_command_0_signals(mock_load_spice_raw, runner):
    """Test the 'init' command with a raw file containing 0 signals."""
    # Arrange - Mock xarray Dataset with no data vars or coordinates
    mock_dataset = xr.Dataset(data_vars={}, coords={})
    mock_load_spice_raw.return_value = mock_dataset

    with runner.isolated_filesystem():
        with open("dummy.raw", "w") as f:
            f.write("dummy data")

        # Act
        result = runner.invoke(cli, ["init", "dummy.raw"])

        # Assert
        assert result.exit_code == 1
        assert "Error: No signals found" in result.output


def test_init_command_file_not_found(runner):
    """Test the 'init' command with a non-existent raw file."""
    # Act
    result = runner.invoke(cli, ["init", "non_existent.raw"])

    # Assert
    assert result.exit_code == 2
    assert "Invalid value for 'RAW_FILE'" in result.output
