import os
import pandas as pd
import pytest
from unittest.mock import patch
from utils import *

@pytest.fixture
def sample_df():
    """
    Fixture pytest yang mengembalikan DataFrame contoh
    yang akan digunakan untuk pengujian fungsi load.
    """
    return pd.DataFrame({
        "Product": ["A", "B"],
        "Price": [10000, 20000]
    })


def test_load_to_csv_success(sample_df):
    """
    Test fungsi load_to_csv untuk memastikan DataFrame disimpan ke file CSV dengan benar.

    Langkah test:
    1. Simpan DataFrame ke CSV.
    2. Pastikan file CSV dibuat.
    3. Baca kembali file CSV dan bandingkan isinya dengan DataFrame awal.
    4. Hapus file setelah test selesai.
    """
    filename = 'testing_loadcsv.csv'
    load_to_csv(sample_df, filename)
    assert os.path.exists(filename)

    df_loaded = pd.read_csv(filename)
    pd.testing.assert_frame_equal(sample_df, df_loaded)

    os.remove(filename)


def test_load_to_csv_failure(sample_df, capsys):
    """
    Test jalur gagal fungsi load_to_csv ketika terjadi exception saat menyimpan file.
    Gunakan mock untuk memaksa df.to_csv melempar Exception.
    """
    with patch.object(pd.DataFrame, "to_csv", side_effect=Exception("Simulasi error")):
        load_to_csv(sample_df, "dummy.csv")
        
        # Tangkap output dari print()
        captured = capsys.readouterr()
        assert "❌ Gagal menyimpan ke CSV: Simulasi error" in captured.out
