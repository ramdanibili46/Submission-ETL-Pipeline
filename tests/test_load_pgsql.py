import os
import pandas as pd
import pytest
from unittest.mock import patch, MagicMock
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


@patch("utils.load_pgsql.create_engine")
def test_load_to_pgrsql(mock_create_engine, sample_df):
    """
    Test fungsi load_to_pgrsql dengan mocking engine dan method to_sql DataFrame.

    Langkah test:
    1. Mock objek engine yang dikembalikan oleh create_engine.
    2. Mock method to_sql langsung di objek sample_df agar memeriksa pemanggilan dengan benar.
    3. Panggil load_to_pgrsql dengan sample_df dan string koneksi dummy.
    4. Pastikan create_engine dipanggil sekali.
    5. Pastikan to_sql dipanggil dengan parameter yang tepat.
    """
    mock_engine = MagicMock()
    mock_create_engine.return_value = mock_engine

    # Mocking method to_sql dari DataFrame (langsung di objek sample_df)
    with patch.object(sample_df, "to_sql") as mock_to_sql:
        load_to_pgrsql(sample_df, "postgresql://user:pass@localhost/dbname")

        mock_create_engine.assert_called_once()
        mock_to_sql.assert_called_once_with(
            'Data_Produk',
            mock_engine,
            index=False,
            if_exists='replace'
        )


@patch("utils.load_pgsql.create_engine", side_effect=Exception("DB error"))
def test_load_to_pgrsql_failure(mock_engine, sample_df, capsys):
    """
    Test skenario kegagalan pada load_to_pgrsql saat terjadi exception dari create_engine.

    Langkah test:
    1. Mock create_engine agar selalu raise Exception.
    2. Panggil load_to_pgrsql, yang seharusnya menangkap exception dan menampilkan pesan error.
    3. Tangkap output stdout menggunakan capsys.
    4. Pastikan pesan error sesuai dengan exception yang dilempar.
    """
    load_to_pgrsql(sample_df, "dummy_string")

    captured = capsys.readouterr()
    assert "❌ Gagal menyimpan ke PostgreSQL: DB error" in captured.out
