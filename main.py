from utils import *

def main():
    BASE_URL = 'https://fashion-studio.dicoding.dev/'
    data = scrape_product(BASE_URL, delay=0)
    df = clean_data_pipeline(data)
    load_to_csv(df, 'Products.csv')
    
    load_to_gsheet(df=df, spreadsheet_id='1dCHFCBmOYmTglq9WqnNy0NKdTs_1nn_xYagcDBweRbU',
                   range_name='Sheet1!A1',
                   credential_file='lithe-quest-496015-n6-91dc6b9418e6.json')
    
    load_to_pgrsql(
    df=df,
    connection_string='postgresql+psycopg2://warudbs:250204@localhost:5432/database_1'
    
)

    
if __name__ == '__main__':
    main()