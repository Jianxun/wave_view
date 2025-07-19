import pytest
from click.testing import CliRunner
from unittest.mock import patch
from wave_view.cli import cli

@pytest.fixture
def runner():
    return CliRunner()

@patch('wave_view.cli.load_spice_raw')
def test_init_command_happy_path(mock_load_spice_raw, runner):
    """Test the 'init' command with a standard raw file."""
    # Arrange
    mock_load_spice_raw.return_value = ({"time": [], "v(out)": [], "v(in)": []}, {})
    
    with runner.isolated_filesystem():
        with open('dummy.raw', 'w') as f:
            f.write('dummy data')
            
        # Act
        result = runner.invoke(cli, ['init', 'dummy.raw'])
        
        # Assert
        assert result.exit_code == 0
        assert 'title: "Analysis of dummy.raw"' in result.output
        assert 'signal: "time"' in result.output
        assert 'v(out): "v(out)"' in result.output
        assert 'v(in): "v(in)"' in result.output
        assert '# Independent variable of the simulation' in result.output 

@patch('wave_view.cli.load_spice_raw')
def test_init_command_2_signals(mock_load_spice_raw, runner):
    """Test the 'init' command with a raw file containing 2 signals."""
    # Arrange
    mock_load_spice_raw.return_value = ({"time": [], "v(out)": []}, {})
    
    with runner.isolated_filesystem():
        with open('dummy.raw', 'w') as f:
            f.write('dummy data')
            
        # Act
        result = runner.invoke(cli, ['init', 'dummy.raw'])
        
        # Assert
        assert result.exit_code == 0
        assert 'signal: "time"' in result.output
        assert 'v(out): "v(out)"' in result.output
        assert 'v(in): "v(in)"' not in result.output 

@patch('wave_view.cli.load_spice_raw')
def test_init_command_1_signal(mock_load_spice_raw, runner):
    """Test the 'init' command with a raw file containing 1 signal."""
    # Arrange
    mock_load_spice_raw.return_value = ({"time": []}, {})
    
    with runner.isolated_filesystem():
        with open('dummy.raw', 'w') as f:
            f.write('dummy data')
            
        # Act
        result = runner.invoke(cli, ['init', 'dummy.raw'])
        
        # Assert
        assert result.exit_code == 0
        assert 'signal: "time"' in result.output
        assert 'signals: {}' in result.output 

@patch('wave_view.cli.load_spice_raw')
def test_init_command_0_signals(mock_load_spice_raw, runner):
    """Test the 'init' command with a raw file containing 0 signals."""
    # Arrange
    mock_load_spice_raw.return_value = ({}, {})
    
    with runner.isolated_filesystem():
        with open('dummy.raw', 'w') as f:
            f.write('dummy data')
            
        # Act
        result = runner.invoke(cli, ['init', 'dummy.raw'])
        
        # Assert
        assert result.exit_code == 1
        assert "Error: No signals found" in result.output 

def test_init_command_file_not_found(runner):
    """Test the 'init' command with a non-existent raw file."""
    # Act
    result = runner.invoke(cli, ['init', 'non_existent.raw'])
    
    # Assert
    assert result.exit_code == 2
    assert "Invalid value for 'RAW_FILE'" in result.output 