import pandas as pd
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

def load_to_gsheet(df, spreadsheet_id, range_name, credential_file):
    """
    Menyimpan DataFrame ke Google Sheets.

    Args:
        df (pd.DataFrame): Data yang akan disimpan.
        spreadsheet_id (str): ID spreadsheet Google Sheets.
        range_name (str): Range target pada sheet, misalnya 'Sheet1!A1'.
        credential_file (str): Path ke file credentials Google Service Account.
    """
    try:
        creds = Credentials.from_service_account_file(credential_file)
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()

        values = [df.columns.tolist()] + df.astype(str).values.tolist()

        body = {
            'values': values
        }

        result = sheet.values().update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption='RAW', 
            body=body
        ).execute()

        print(f"✅ {result.get('updatedCells')} sel ditambahkan ke Google Sheet!")
    except Exception as e:
        print(f"❌ Gagal menyimpan ke Google Sheets: {e}")
