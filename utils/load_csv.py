import pandas as pd

def load_to_csv(df, csv_name):
    """
    Menyimpan DataFrame ke dalam file CSV.

    Args:
        df (pd.DataFrame): Data yang akan disimpan.
    """
    try:
        df.to_csv(csv_name, index=False)
        print("✅ Data berhasil disimpan ke file CSV.")
    except Exception as e:
        print(f"❌ Gagal menyimpan ke CSV: {e}")