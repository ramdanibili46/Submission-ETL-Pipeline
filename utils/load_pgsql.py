import pandas as pd
from sqlalchemy import create_engine

def load_to_pgrsql(df, connection_string):
    """
    Menyimpan DataFrame ke database PostgreSQL.

    Args:
        df (pd.DataFrame): Data yang akan disimpan.
        connection_string (str): String koneksi PostgreSQL (contoh: postgresql://user:pass@host/db).
    """
    try:
        engine = create_engine(connection_string)
        df.to_sql('Data_Produk', engine, index=False, if_exists='replace')
        print("✅ Data berhasil disimpan ke PostgreSQL.")
    except Exception as e:
        print(f"❌ Gagal menyimpan ke PostgreSQL: {e}")
