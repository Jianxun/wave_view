import pytest
from unittest.mock import patch, MagicMock

from wave_view.core.wavedataset import WaveDataset, MAX_SIGNALS_TO_SHOW


class TestWaveDatasetErrorPaths:
    """Additional tests that exercise WaveDataset edge/error cases."""

    def _make_dataset_with_signals(self, signal_names):
        """Helper that returns a WaveDataset instance with mocked RawRead."""
        with patch("wave_view.core.wavedataset.RawRead") as mock_raw_read:
            mock_raw = MagicMock()
            mock_raw.get_trace_names.return_value = signal_names
            mock_raw.get_trace.side_effect = lambda name: [0, 1, 2]  # dummy data
            mock_raw_read.return_value = mock_raw
            return WaveDataset.from_raw("dummy.raw")

    def test_get_signal_missing_raises_valueerror(self):
        """get_signal() should raise ValueError with truncated signal list when missing."""
        # Create more signals than MAX_SIGNALS_TO_SHOW to test truncation logic
        signals = [f"sig{i}" for i in range(MAX_SIGNALS_TO_SHOW + 2)]
        dataset = self._make_dataset_with_signals(signals)

        with pytest.raises(ValueError) as excinfo:
            dataset.get_signal("nonexistent")

        msg = str(excinfo.value)
        # It should list only the first MAX_SIGNALS_TO_SHOW signals
        for name in signals[:MAX_SIGNALS_TO_SHOW]:
            assert name.lower() in msg
        assert "..." in msg  # Ellipsis indicates truncation

    def test_from_raw_file_not_found(self):
        """from_raw() should propagate FileNotFoundError with custom message."""
        with patch("wave_view.core.wavedataset.RawRead", side_effect=FileNotFoundError):
            with pytest.raises(FileNotFoundError):
                WaveDataset.from_raw("missing.raw")

    def test_from_raw_generic_exception_wrapped(self):
        """Any other exception from RawRead should be wrapped with informative message."""
        with patch("wave_view.core.wavedataset.RawRead", side_effect=Exception("boom")):
            with pytest.raises(Exception) as excinfo:
                WaveDataset.from_raw("bad.raw")
        assert "boom" in str(excinfo.value) 