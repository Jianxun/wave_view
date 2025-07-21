import numpy as np
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from yaml2plot import loader as wv_loader


class TestValidateFilePath:
    def test_valid_path_returns_path_instance(self, tmp_path):
        f = tmp_path / "dummy.raw"
        f.write_text("RAW")
        result = wv_loader._validate_file_path(f)
        assert isinstance(result, Path) and result == f

    @pytest.mark.parametrize(
        "bad_input, expected_exc",
        [
            (None, TypeError),
            ("", ValueError),
            (123, TypeError),
        ],
    )
    def test_bad_inputs_raise(self, bad_input, expected_exc):
        with pytest.raises(expected_exc):
            wv_loader._validate_file_path(bad_input)

    def test_nonexistent_file_raises(self, tmp_path):
        ghost = tmp_path / "ghost.raw"
        with pytest.raises(FileNotFoundError):
            wv_loader._validate_file_path(ghost)


class TestLoadSpiceRaw:
    def _mock_dataset(self):
        mock_ds = MagicMock()
        mock_ds.signals = ["time", "v(out)"]
        mock_ds.metadata = {"corner": "tt"}
        mock_ds.get_signal.side_effect = lambda name: np.array([0, 1, 2])
        return mock_ds

    def test_happy_path_returns_data_and_metadata(self, tmp_path):
        f = tmp_path / "sig.raw"
        f.write_text("dummy")
        with patch.object(
            wv_loader.WaveDataset, "from_raw", return_value=self._mock_dataset()
        ) as m_from:
            data, meta = wv_loader.load_spice_raw(f)

        # Verify mapping built correctly
        assert set(data.keys()) == {"time", "v(out)"}
        for arr in data.values():
            np.testing.assert_array_equal(arr, np.array([0, 1, 2]))
        assert meta == {"corner": "tt"}
        m_from.assert_called_once_with(str(f))

    def test_file_not_found_bubbles_up(self):
        with pytest.raises(FileNotFoundError):
            wv_loader.load_spice_raw("/does/not/exist.raw")


class TestLoadSpiceRawBatch:
    def test_batch_calls_underlying_loader(self, tmp_path):
        p1 = tmp_path / "a.raw"
        p2 = tmp_path / "b.raw"
        for p in (p1, p2):
            p.write_text("D")

        with patch.object(
            wv_loader, "load_spice_raw", return_value=({"sig": np.array([1])}, {})
        ) as m_load:
            results = wv_loader.load_spice_raw_batch([p1, p2])

        assert len(results) == 2
        assert m_load.call_count == 2
        m_load.assert_any_call(p1)
        m_load.assert_any_call(p2)

    @pytest.mark.parametrize("bad_input", [None, "not-a-list", 123])
    def test_bad_collections_raise(self, bad_input):
        with pytest.raises(TypeError):
            wv_loader.load_spice_raw_batch(bad_input)
