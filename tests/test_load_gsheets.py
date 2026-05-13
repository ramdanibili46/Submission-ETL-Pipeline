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

@patch("utils.load_gsheets.Credentials.from_service_account_file")
@patch("utils.load_gsheets.build")
def test_load_to_gsheet(mock_build, mock_creds, sample_df):
    """
    Test fungsi load_to_gsheet dengan mocking API Google Sheets.

    Langkah test:
    1. Mock credential loading dari file JSON.
    2. Mock objek service Google Sheets, khususnya method update().execute().
    3. Panggil load_to_gsheet dengan sample_df dan parameter dummy.
    4. Verifikasi method-method penting dipanggil sesuai harapan:
       - Credential dari file dipanggil sekali.
       - Service Google Sheets dibangun sekali.
       - Method update dan execute dijalankan sekali.
    """
    # Mock return value untuk update().execute()
    mock_update = MagicMock()
    mock_update.execute.return_value = {'updatedCells': 4}

    # Mock return value untuk values()
    mock_values = MagicMock()
    mock_values.update.return_value = mock_update

    # Mock return value untuk spreadsheets()
    mock_spreadsheets = MagicMock()
    mock_spreadsheets.values.return_value = mock_values

    # Mock Google Sheets service
    mock_service = MagicMock()
    mock_service.spreadsheets.return_value = mock_spreadsheets

    # Set build() return
    mock_build.return_value = mock_service

    # Jalankan fungsi yang dites
    load_to_gsheet(
        sample_df,
        spreadsheet_id="dummy_id",
        range_name="Sheet1!A1",
        credential_file="dummy_credentials.json"
    )

    # Verifikasi pemanggilan method-method penting
    mock_creds.assert_called_once_with("dummy_credentials.json")
    mock_build.assert_called_once()
    mock_spreadsheets.values.assert_called_once()
    mock_values.update.assert_called_once()
    mock_update.execute.assert_called_once()
