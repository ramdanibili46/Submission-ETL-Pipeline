import pandas as pd
import re

# Pola nilai yang dianggap kotor/tidak valid
DIRTY_PATTERNS = {
    "Title": ["Unknown Product"],
    "Rating": ["Invalid Rating / 5", "Not Rated"],
    "Price": ["Price Unavailable", None]
}

def remove_dirty_values(df, patterns=DIRTY_PATTERNS):
    """
    Menghapus baris pada DataFrame yang mengandung nilai tidak valid.

    Args:
        df (pd.DataFrame): Data mentah.
        patterns (dict): Dictionary berisi nilai-nilai yang dianggap tidak valid untuk setiap kolom.

    Returns:
        pd.DataFrame: Data yang sudah dibersihkan dari nilai-nilai tidak valid.
    """
    try:
        for column, dirty_values in patterns.items():
            df = df[~df[column].isin(dirty_values)]
        return df.reset_index(drop=True)
    except Exception as e:
        raise ValueError(f"Gagal menghapus nilai tidak valid: {e}")

def clean_price(df, multiplier=16000):
    """
    Membersihkan kolom harga dari simbol dan mengkonversi ke rupiah.

    Args:
        df (pd.DataFrame): DataFrame dengan kolom 'Price'.
        multiplier (int): Nilai tukar USD ke IDR.

    Returns:
        pd.DataFrame: DataFrame dengan kolom 'Price' dalam rupiah.
    """
    try:
        df['Price'] = df['Price'].str.replace('$', '', regex=False).astype(float)
        df['Price'] *= multiplier
        return df
    except Exception as e:
        raise ValueError(f"Gagal membersihkan kolom Price: {e}")

def clean_rating(df):
    """
    Mengekstrak nilai rating dari string dan mengubah ke float.

    Args:
        df (pd.DataFrame): DataFrame dengan kolom 'Rating'.

    Returns:
        pd.DataFrame: DataFrame dengan kolom 'Rating' bertipe float.
    """
    try:
        df['Rating'] = df['Rating'].str.extract(r'⭐ ([0-9]+\.[0-9])')[0]
        df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
        df = df.dropna(subset=['Rating'])
        return df
    except Exception as e:
        raise ValueError(f"Gagal membersihkan kolom Rating: {e}")

def clean_colors(df):
    """
    Mengekstrak jumlah warna dari string dan mengubah ke integer.

    Args:
        df (pd.DataFrame): DataFrame dengan kolom 'Colors'.

    Returns:
        pd.DataFrame: DataFrame dengan kolom 'Colors' bertipe int.
    """
    try:
        df['Colors'] = df['Colors'].str.extract(r'(\d+)').astype(int)
        return df
    except Exception as e:
        raise ValueError(f"Gagal membersihkan kolom Colors: {e}")

def clean_size(df):
    """
    Menghapus awalan 'Size: ' pada kolom ukuran pakaian.

    Args:
        df (pd.DataFrame): DataFrame dengan kolom 'Size'.

    Returns:
        pd.DataFrame: DataFrame dengan kolom 'Size' yang telah dibersihkan.
    """
    try:
        df['Size'] = df['Size'].str.replace('Size: ', '', regex=False)
        return df
    except Exception as e:
        raise ValueError(f"Gagal membersihkan kolom Size: {e}")

def clean_gender(df):
    """
    Menghapus awalan 'Gender: ' pada kolom gender.

    Args:
        df (pd.DataFrame): DataFrame dengan kolom 'Gender'.

    Returns:
        pd.DataFrame: DataFrame dengan kolom 'Gender' yang telah dibersihkan.
    """
    try:
        df['Gender'] = df['Gender'].str.replace('Gender: ', '', regex=False)
        return df
    except Exception as e:
        raise ValueError(f"Gagal membersihkan kolom Gender: {e}")

def format_timestamp(df):
    """
    Memformat kolom 'Timestamp' menjadi string format ISO 8601.

    Args:
        df (pd.DataFrame): DataFrame dengan kolom 'Timestamp'.

    Returns:
        pd.DataFrame: DataFrame dengan kolom 'Timestamp' terformat.
    """
    try:
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        df['Timestamp'] = df['Timestamp'].dt.strftime('%Y-%m-%dT%H:%M:%S.%f')
        return df
    except Exception as e:
        raise ValueError(f"Gagal memformat kolom Timestamp: {e}")

def drop_unwanted(df):
    """
    Menghapus duplikat dan baris dengan nilai kosong.

    Args:
        df (pd.DataFrame): DataFrame yang ingin dibersihkan.

    Returns:
        pd.DataFrame: DataFrame tanpa duplikat dan nilai kosong.
    """
    try:
        df = df.dropna()
        df = df.drop_duplicates()
        return df
    except Exception as e:
        raise ValueError(f"Gagal menghapus nilai kosong/duplikat: {e}")

def clean_data_pipeline(df):
    """
    Menjalankan semua tahapan pembersihan data dalam satu alur.

    Tahapan:
    1. Hapus data tidak valid.
    2. Bersihkan harga dan konversi ke IDR.
    3. Ekstrak rating.
    4. Ekstrak jumlah warna.
    5. Bersihkan ukuran.
    6. Bersihkan gender.
    7. Format waktu.
    8. Hapus NaN dan duplikat.

    Args:
        df (pd.DataFrame): Data awal hasil scraping.

    Returns:
        pd.DataFrame: Data yang telah bersih dan siap digunakan.
    """
    try:
        df = pd.DataFrame(df)
        df = remove_dirty_values(df)
        df = clean_price(df)
        df = clean_rating(df)
        df = clean_colors(df)
        df = clean_size(df)
        df = clean_gender(df)
        df = format_timestamp(df)
        df = drop_unwanted(df)
        print("✅ Data Berhasil ditransformasi.")
        return df
    except Exception as e:
        raise ValueError(f"Gagal menjalankan pipeline pembersihan data: {e}")
