import pytest
import pandas as pd
import datetime
from utils import *

DIRTY_PATTERNS = {
    "Title": ["Unknown Product"],
    "Rating": ["Invalid Rating / 5", "Not Rated"],
    "Price": ["Price Unavailable", None]
}

@pytest.fixture
def sample_data():
    return pd.DataFrame({
        "Title": ["Book", "Unknown Product", "Good Product"],
        "Price": ["$10.5", "Price Unavailable", None],
        "Rating": ["⭐ 4.5", "Invalid Rating / 5", "Not Rated"],
        "Colors": ["3 colors", "5 colors", "2 colors"],
        "Size": ["Size: M", "Size: L", "Size: S"],
        "Gender": ["Gender: Men", "Gender: Women", "Gender: Men"],
        "Timestamp": [datetime.datetime.now()] * 3,
    })


def test_remove_dirty_values(sample_data):
    cleaned = remove_dirty_values(sample_data, patterns=DIRTY_PATTERNS)
    assert "Unknown Product" not in cleaned["Title"].values
    assert "Price Unavailable" not in cleaned["Price"].values
    assert None not in cleaned["Price"].values
    assert "Invalid Rating / 5" not in cleaned["Rating"].values
    assert "Not Rated" not in cleaned["Rating"].values


def test_clean_price():
    df = pd.DataFrame({"Price": ["$1.0", "$2.5"]})
    cleaned = clean_price(df.copy(), multiplier=1000)
    assert all(cleaned["Price"] == pd.Series([1000.0, 2500.0]))

def test_clean_price_invalid_type():
    df = pd.DataFrame({"Price": [1000, 2000]})  # bukan string
    with pytest.raises(ValueError, match="Gagal membersihkan kolom Price"):
        clean_price(df)
        
def test_clean_price_empty_df():
    df = pd.DataFrame(columns=["Price"])
    cleaned = clean_price(df.copy())
    assert cleaned.empty

def test_clean_price_missing_column():
    df = pd.DataFrame({"NotPrice": ["$10"]})
    with pytest.raises(ValueError):
        clean_price(df)

def test_clean_rating():
    df = pd.DataFrame({"Rating": ["⭐ 4.5", "⭐ 3.0", "Invalid"]})
    cleaned = clean_rating(df.copy())
    assert all(cleaned["Rating"].between(3.0, 4.5))
    assert cleaned.shape[0] == 2  # baris dengan "Invalid" harus hilang

def test_clean_colors():
    df = pd.DataFrame({"Colors": ["3", "10", "abc"]})
    with pytest.raises(ValueError):
        clean_colors(df.copy())
    df_valid = pd.DataFrame({"Colors": ["3", "10"]})
    cleaned = clean_colors(df_valid.copy())
    assert all(cleaned["Colors"] == pd.Series([3, 10]))

def test_clean_size():
    df = pd.DataFrame({"Size": ["Size: M", "Size: L"]})
    cleaned = clean_size(df.copy())
    assert all(cleaned["Size"] == pd.Series(["M", "L"]))

def test_clean_gender():
    df = pd.DataFrame({"Gender": ["Gender: Men", "Gender: Women"]})
    cleaned = clean_gender(df.copy())
    assert all(cleaned["Gender"] == pd.Series(["Men", "Women"]))

def test_format_timestamp():
    now = datetime.datetime(2025, 5, 17, 15, 30, 45, 123456)
    df = pd.DataFrame({"Timestamp": [now]})
    cleaned = format_timestamp(df.copy())
    assert cleaned["Timestamp"].iloc[0] == "2025-05-17T15:30:45.123456"
    
def test_drop_unwanted():
    df = pd.DataFrame({
        "A": [1, 2, None, 2],
        "B": [None, "x", "y", "x"]
    })
    cleaned = drop_unwanted(df.copy())
    # harus drop row dengan None dan duplikat
    assert cleaned.shape[0] == 1
    assert cleaned.iloc[0]["A"] == 2

def test_clean_data_pipeline(sample_data):
    cleaned = clean_data_pipeline(sample_data)
    # Pastikan data sudah bersih dari nilai kotor dan kolom sudah tertransformasi
    assert "Unknown Product" not in cleaned["Title"].values
    assert all(cleaned["Price"] > 0)
    assert cleaned["Rating"].dtype == float
    assert cleaned["Colors"].dtype == int
    assert not cleaned.isnull().values.any()

def test_pipeline_failure():
    df = pd.DataFrame({"UnknownCol": ["abc"]})
    with pytest.raises(ValueError, match="Gagal menjalankan pipeline pembersihan data"):
        clean_data_pipeline(df)
