"""
Tests for the WaveformViewer class.
"""

import pytest
from src.wave_view.viewer import WaveformViewer


class TestWaveformViewer:
    """Test cases for WaveformViewer class."""
    
    def test_init_empty(self):
        """Test initialization without data."""
        viewer = WaveformViewer()
        assert viewer._data is None
        assert viewer._signals == []
        
    def test_init_with_data(self):
        """Test initialization with data."""
        test_data = {"test": "data"}
        viewer = WaveformViewer(data=test_data)
        assert viewer._data == test_data
        assert viewer._signals == []
        
    def test_add_signal(self):
        """Test adding signals."""
        viewer = WaveformViewer()
        viewer.add_signal("voltage")
        assert "voltage" in viewer.get_signals()
        
    def test_add_duplicate_signal(self):
        """Test adding duplicate signals."""
        viewer = WaveformViewer()
        viewer.add_signal("voltage")
        viewer.add_signal("voltage")
        assert viewer.get_signals().count("voltage") == 1
        
    def test_get_signals_returns_copy(self):
        """Test that get_signals returns a copy, not reference."""
        viewer = WaveformViewer()
        viewer.add_signal("voltage")
        signals = viewer.get_signals()
        signals.append("current")
        assert "current" not in viewer.get_signals()
        
    def test_load_data_not_implemented(self):
        """Test that load_data raises NotImplementedError."""
        viewer = WaveformViewer()
        with pytest.raises(NotImplementedError):
            viewer.load_data("test_file.raw")
            
    def test_plot_not_implemented(self):
        """Test that plot raises NotImplementedError."""
        viewer = WaveformViewer()
        with pytest.raises(NotImplementedError):
            viewer.plot() 