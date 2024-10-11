import pandas as pd

def convert_xlsx_to_csv(xlsx_file):
    # Read the Excel file
    df = pd.read_excel(xlsx_file)  # Reads all sheets
    df.dropna(inplace=True)
    df.to_csv("stock_list/filtered_mother_baby.csv")

if __name__ == "__main__":
    xlsx_file = "stock_list/mother_baby_stock.xlsx"  # Replace with your .xlsx file
    convert_xlsx_to_csv(xlsx_file)
    print("Conversion complete!")
