import pandas as pd

def convert_xlsx_to_csv(xlsx_file, csv_file):
    # Read the Excel file
    df = pd.read_excel(xlsx_file)  # Reads all sheets
    df.dropna(inplace=True)
    df.to_csv("filtered_mother_baby.csv")

if __name__ == "__main__":
    xlsx_file = "mother_baby_stock.xlsx"  # Replace with your .xlsx file
    csv_file = "mother_baby_stock"       # Base name for the output .csv files
    convert_xlsx_to_csv(xlsx_file, csv_file)
    print("Conversion complete!")
