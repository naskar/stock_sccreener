import requests
from datetime import datetime, timedelta
import pandas as pd
import yfinance as yf
import time
import numpy as np


def color_text_one_year(val):
    if val >= 20:
        return 'color: green;'  # Change color to green for values > 100
    elif val<0:
        return 'color: red;' 
    else:
        return 'color: blue;' 
    
def color_text(val):
    if val >= 100:
        return 'color: green;'  # Change color to green for values > 100
    else:
        return 'color: blue;' 

def last_year_return(stock_data):
    diff_percentage = (((stock_data["mother_live_price"] - stock_data["mother_1year_close"]) * 100) / stock_data["mother_1year_close"])
    stock_data["mother_one_year_return"] = round(diff_percentage, 2)


def deduce_mother(prev_high, prev_low, today_high, today_low, prev_open, prev_close):
    if today_high<prev_high and prev_low<today_low:
        if prev_open<prev_close:
            return True
        else:
            return False
    else:
        return False



def calculate_rsi(data, period=14):
    # Calculate price difference
    delta = data['Close'].diff()

    # Separate positive gains and negative losses
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)

    # Calculate the average gain and loss
    avg_gain = pd.Series(gain).rolling(window=period, min_periods=1).mean()
    avg_loss = pd.Series(loss).rolling(window=period, min_periods=1).mean()

    # Calculate the Relative Strength (RS)
    rs = avg_gain / avg_loss

    # Calculate the RSI
    rsi = 100 - (100 / (1 + rs))
    return rsi

def get_today_price(stock_data):
    stock = yf.Ticker(stock_data["Symbol"] + ".NS")
    historical_two_days_info = stock.history(period="5d")
    # Fetch live price data
    stock_info = stock.history(period="1d", interval="1m")  # 1-minute interval for near real-time da
    mother_baby_cond = deduce_mother(prev_high=float(historical_two_days_info['High'].iloc[-2]), prev_low=float(historical_two_days_info['Low'].iloc[-2]), today_high=stock_info['High'].max(), today_low=stock_info['Low'].min(), prev_close=float(historical_two_days_info['Close'].iloc[-2]), prev_open=float(historical_two_days_info['Open'].iloc[-2]))
    if not stock_info.empty and mother_baby_cond:
        current_price = stock_info['Close'].iloc[-1]  # Get the latest close price (most recent minute)
        open_price = stock_info['Open'].iloc[0]  # Open price of the day
        high_price = stock_info['High'].max()    # Highest price of the day
        low_price = stock_info['Low'].min()      # Lowest price of the day
        # Calculate RSI
        # Fetch data for the previous 2 days (yesterday and today)
        historical_info = stock.history(period="1y")
        historical_info.drop(index=historical_info.index[-1], axis=0, inplace=True)
        latest_rsi = calculate_rsi(historical_info).iloc[-1]   
        stock_data["mother_live_price"] =round(float(current_price), 2)
        stock_data["mother_today_open_price"] = round(float(open_price), 2)
        stock_data["mother_today_high"] = round(float(high_price), 2)
        stock_data["mother_today_low"] =round (float(low_price), 2)
        stock_data["mother_RSI"] = round(float(latest_rsi), 2)
        stock_data["mother_previous_close"] =round(float(historical_info['Close'].iloc[-2]), 2)
        stock_data["mother_previous_high"] = round(float(historical_info['High'].iloc[-2]), 2)
        stock_data["mother_previous_low"] = round(float(historical_info['Low'].iloc[-2]), 2)
        stock_data["mother_1year_close"] = round(float(historical_info['Close'].iloc[0]), 2)
        stock_data["mother_previous_open"] = round(float(historical_info['Open'].iloc[-2]), 2)
        last_year_return(stock_data=stock_data)
        print(f"stock data processing completed for - {stock_data['Symbol']}")

    else:
        print(f"stock data proessing completed for - {stock_data['Symbol']}")
        stock_data = {}
        

#
# Example usage
if __name__ == "__main__":
    stock_list = pd.read_csv("stock_list/nifty_100.csv").to_dict(orient="records")
    try:
        for item in stock_list:
            stock_data = get_today_price(stock_data = item)
    except Exception as e:
        print(e)
    print("Excel sheet data is prepared")
    stock_list_df = pd.DataFrame(stock_list)
    stock_list_df.dropna(subset=["mother_live_price"], inplace=True)
    stock_list_df.drop(["mother_1year_close"], axis = 1, inplace=True)
    stock_list_df = (
        stock_list_df.style
        .map(color_text, subset=['mother_live_price'])
        .map(color_text_one_year, subset=['mother_one_year_return'])
    )
    stock_list_df.to_excel('stock_list/mother_baby_stock.xlsx', engine='xlsxwriter', index=False)
    print("Exported mother_baby_stock Excel")
    # html = stock_list_df.to_html()

    # # write html to file
    # text_file = open("index.html", "w")
    # text_file.write(html)
    # text_file.close()