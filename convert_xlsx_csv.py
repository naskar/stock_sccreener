import pandas as pd

from mother_baby_filter import color_text_one_year, color_text_price

def convert_xlsx_to_csv(xlsx_file):
    # Read the Excel file
    df = pd.read_excel(xlsx_file)  # Reads all sheets
    df.dropna(inplace=True)
    df = df[["Company Name", "Industry", "Symbol", "mother_live_price", "mother_one_year_return"]]
    df.rename(columns={'mother_live_price': 'price', 'mother_one_year_return': 'one_yr_return'}, inplace=True)
    df = (
        df.style
        .map(color_text_one_year, subset=['one_yr_return'])
        .map(color_text_price, subset=['price'])
    )
    df.to_excel('stock_list/sheet1.xlsx', engine='xlsxwriter', index=False)
if __name__ == "__main__":
    xlsx_file = "stock_list/mother_baby_stock.xlsx"  # Replace with your .xlsx file
    convert_xlsx_to_csv(xlsx_file)
    print("Conversion complete!")
