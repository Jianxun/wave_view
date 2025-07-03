"""Test cases for WaveDataset class."""

import pytest
import numpy as np
from pathlib import Path
from unittest.mock import patch, MagicMock

from wave_view.core.wavedataset import WaveDataset


class TestWaveDatasetFromRaw:
    """Test WaveDataset.from_raw() factory method."""
    
    def test_from_raw_creates_wavedataset_instance(self):
        """Test that from_raw() creates a WaveDataset instance."""
        # Mock the RawRead to avoid needing actual raw files
        with patch('wave_view.core.wavedataset.RawRead') as mock_rawread:
            mock_rawread.return_value = MagicMock()
            
            # Test the factory method
            dataset = WaveDataset.from_raw("test.raw")
            
            # Should create a WaveDataset instance
            assert isinstance(dataset, WaveDataset)
            
            # Should have called RawRead with the file path
            mock_rawread.assert_called_once_with("test.raw")
    
    def test_from_raw_with_metadata(self):
        """Test that from_raw() accepts optional metadata."""
        # Mock the RawRead to avoid needing actual raw files
        with patch('wave_view.core.wavedataset.RawRead') as mock_rawread:
            mock_rawread.return_value = MagicMock()
            
            # Test with metadata
            metadata = {"temperature": 25, "corner": "tt"}
            dataset = WaveDataset.from_raw("test.raw", metadata=metadata)
            
            # Should create a WaveDataset instance
            assert isinstance(dataset, WaveDataset)
            
            # Should have called RawRead with the file path
            mock_rawread.assert_called_once_with("test.raw")


class TestWaveDatasetSignals:
    """Test WaveDataset signals property."""
    
    def test_signals_property_returns_lowercase_signal_names(self):
        """Test that signals property returns normalized lowercase signal names."""
        # Mock RawRead with test signal names
        with patch('wave_view.core.wavedataset.RawRead') as mock_rawread:
            mock_raw_data = MagicMock()
            mock_raw_data.get_trace_names.return_value = ["Time", "V(out)", "I(Vin)", "V(VDD)"]
            mock_rawread.return_value = mock_raw_data
            
            # Create WaveDataset
            dataset = WaveDataset.from_raw("test.raw")
            
            # Should return normalized lowercase signal names
            expected_signals = ["time", "v(out)", "i(vin)", "v(vdd)"]
            assert dataset.signals == expected_signals
            
            # Should have called get_trace_names
            mock_raw_data.get_trace_names.assert_called_once()


class TestWaveDatasetGetSignal:
    """Test WaveDataset get_signal() method."""
    
    def test_get_signal_returns_numpy_array(self):
        """Test that get_signal() returns signal data as numpy array."""
        # Mock RawRead with test signal data
        with patch('wave_view.core.wavedataset.RawRead') as mock_rawread:
            mock_raw_data = MagicMock()
            mock_raw_data.get_trace_names.return_value = ["Time", "V(out)"]
            mock_raw_data.get_trace.return_value = [0.0, 1.0, 2.0, 3.0]
            mock_rawread.return_value = mock_raw_data
            
            # Create WaveDataset
            dataset = WaveDataset.from_raw("test.raw")
            
            # Should return signal data as numpy array
            signal_data = dataset.get_signal("V(out)")
            
            # Should be a numpy array
            assert isinstance(signal_data, np.ndarray)
            
            # Should have the correct data
            expected_data = np.array([0.0, 1.0, 2.0, 3.0])
            np.testing.assert_array_equal(signal_data, expected_data)
            
            # Should have called get_trace with the original case signal name
            mock_raw_data.get_trace.assert_called_once_with("V(out)")
    
    def test_get_signal_case_insensitive(self):
        """Test that get_signal() works with case-insensitive signal names."""
        # Mock RawRead with test signal data
        with patch('wave_view.core.wavedataset.RawRead') as mock_rawread:
            mock_raw_data = MagicMock()
            mock_raw_data.get_trace_names.return_value = ["Time", "V(out)"]
            mock_raw_data.get_trace.return_value = [0.0, 1.0, 2.0, 3.0]
            mock_rawread.return_value = mock_raw_data
            
            # Create WaveDataset
            dataset = WaveDataset.from_raw("test.raw")
            
            # Should work with lowercase input
            signal_data = dataset.get_signal("v(out)")
            
            # Should be a numpy array with correct data
            assert isinstance(signal_data, np.ndarray)
            expected_data = np.array([0.0, 1.0, 2.0, 3.0])
            np.testing.assert_array_equal(signal_data, expected_data)
            
            # Should have called get_trace with the original case signal name
            mock_raw_data.get_trace.assert_called_once_with("V(out)")


class TestWaveDatasetHasSignal:
    """Test WaveDataset has_signal() method."""
    
    def test_has_signal_returns_true_for_existing_signal(self):
        """Test that has_signal() returns True for existing signals."""
        # Mock RawRead with test signal names
        with patch('wave_view.core.wavedataset.RawRead') as mock_rawread:
            mock_raw_data = MagicMock()
            mock_raw_data.get_trace_names.return_value = ["Time", "V(out)", "I(Vin)"]
            mock_rawread.return_value = mock_raw_data
            
            # Create WaveDataset
            dataset = WaveDataset.from_raw("test.raw")
            
            # Should return True for existing signals
            assert dataset.has_signal("V(out)") is True
            assert dataset.has_signal("v(out)") is True  # Case insensitive
            assert dataset.has_signal("I(Vin)") is True
            assert dataset.has_signal("time") is True
    
    def test_has_signal_returns_false_for_nonexistent_signal(self):
        """Test that has_signal() returns False for non-existent signals."""
        # Mock RawRead with test signal names
        with patch('wave_view.core.wavedataset.RawRead') as mock_rawread:
            mock_raw_data = MagicMock()
            mock_raw_data.get_trace_names.return_value = ["Time", "V(out)"]
            mock_rawread.return_value = mock_raw_data
            
            # Create WaveDataset
            dataset = WaveDataset.from_raw("test.raw")
            
            # Should return False for non-existent signals
            assert dataset.has_signal("V(in)") is False
            assert dataset.has_signal("nonexistent") is False


class TestWaveDatasetMetadata:
    """Test WaveDataset metadata property."""
    
    def test_metadata_property_returns_empty_dict_by_default(self):
        """Test that metadata property returns empty dict when no metadata provided."""
        # Mock RawRead 
        with patch('wave_view.core.wavedataset.RawRead') as mock_rawread:
            mock_rawread.return_value = MagicMock()
            
            # Create WaveDataset without metadata
            dataset = WaveDataset.from_raw("test.raw")
            
            # Should return empty dict
            assert dataset.metadata == {}
            
    def test_metadata_property_returns_provided_metadata(self):
        """Test that metadata property returns the provided metadata."""
        # Mock RawRead
        with patch('wave_view.core.wavedataset.RawRead') as mock_rawread:
            mock_rawread.return_value = MagicMock()
            
            # Create WaveDataset with metadata
            test_metadata = {"temperature": 25, "corner": "tt", "process": "nominal"}
            dataset = WaveDataset.from_raw("test.raw", metadata=test_metadata)
            
            # Should return the provided metadata
            assert dataset.metadata == test_metadata
            
            # Should be a copy, not the same object
            assert dataset.metadata is not test_metadata 