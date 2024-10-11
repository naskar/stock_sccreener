import pandas as pd
import yfinance as yf

from mother_baby_filter import calculate_rsi
import time


def color_text(val):
    if val == True:
        return 'color: green;'  # Change color to green for values > 100
    else:
        return 'color: Pink;'
    
def color_text_value(val):
    if val == "High":
        return 'color: green;'  # Change color to green for values > 100
    if val == "Low":
        return 'color: Pink;'

def get_screener_condition_col(stock_data):
    stock = yf.Ticker(stock_data["Symbol"] + ".NS")
    print(f"Conditionl formation started for - {stock}")
    screener_stock_details = {}
    screener_stock_details["Company Name"]  = stock_data["Company Name"]
    screener_stock_details["Industry"]  = stock_data["Industry"]
    screener_stock_details["Symbol"]  = stock_data["Symbol"]

    comp_data = (stock_data["mother_previous_high"] * 5) / 100
    if stock_data["mother_previous_high"] - stock_data["mother_previous_low"] >= comp_data:
        screener_stock_details["high or low"] = 'High'
    else:
        screener_stock_details["high or low"] = 'Low'
    screener_stock_details["Actual Target"] =  round((stock_data["mother_previous_high"] + (2 * stock_data["mother_previous_high"] - stock_data["mother_previous_low"])), 2)
    stock_info = stock.history(period="1d", interval="1m")  # 1-minute interval for near real-time
    screener_stock_details["live_price"] = round((float(stock_info['Close'].iloc[-1])), 2)
    real_price = (float(stock_info['Close'].iloc[-1]) * 105) / 100
    screener_stock_details["five_percent_Target"] = round(real_price, 2)

    if screener_stock_details["Actual Target"] > screener_stock_details["five_percent_Target"]:
        screener_stock_details["Price Crossover"] = True
    else:
        screener_stock_details["Price Crossover"] = False
    nine_five_of_real_price = (stock_info['Close'].iloc[-1] * 95) / 100
    if stock_data["mother_previous_low"] > nine_five_of_real_price:
        screener_stock_details["RR Ratio"] = True
    else:
        screener_stock_details["RR Ratio"] = False
    
    historical_info = stock.history(period="1y")
    current_rsi = calculate_rsi(historical_info).iloc[-1]
    if current_rsi >  stock_data["mother_RSI"] :
        screener_stock_details["RSI Cross over"] = True
    else:
        screener_stock_details["RSI Cross over"] = False
    return screener_stock_details




if __name__ == "__main__":
    while True:
        stock_list = pd.read_csv("stock_list/filtered_mother_baby.csv").to_dict(orient="records")
        stock_data_list = []
        try:
            for item in stock_list:
                stock_data_list.append(get_screener_condition_col(stock_data = item))
        except Exception as e:
            print(e)

        stock_list_df = pd.DataFrame(stock_data_list)
        stock_list_df = (
            stock_list_df.style
            .map(color_text, subset=['RR Ratio', 'RSI Cross over', 'Price Crossover'])
            .map(color_text_value, subset=['high or low'])
        )
        html = stock_list_df.to_html()

        # write html to file
        text_file = open("index.html", "w")
        text_file.write(html)
        text_file.close()
        print("Process Completed .... Price will be updated after 1 minute")
        time.sleep(60)