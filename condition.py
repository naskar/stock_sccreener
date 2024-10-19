import os
import pandas as pd
import yfinance as yf

from mother_baby_filter import calculate_rsi
import time

def color_text_sector_trend(val):
    if val == "sector_trend>0":
        return 'color: green;'  # Change color to green for values > 100
    elif val == "sector_trend<0":
        return 'color: Pink;'
    elif val == "sector_trend=0":
        return 'color: Blue;'

def color_text_nifty_trend(val):
    if val == "nifty_trend>0":
        return 'color: green;'  # Change color to green for values > 100
    elif val == "nifty_trend<0":
        return 'color: Pink;'
    elif val == "nifty_trend=0":
        return 'color: Blue;'

def color_text_resistance(val):
    if val == "resistance>0":
        return 'color: green;'  # Change color to green for values > 100
    elif val == "resistance<0":
        return 'color: Pink;'
    elif val == "resistance=0":
        return 'color: Blue;'

# def live_price_calc(stock_data):
#     stock = yf.Ticker(stock_data["Symbol"] + ".NS")
#     stock_info = stock.history(period="1d", interval="1m")  # 1-minute interval for near real-time
#     stock_data["Price"] = round((float(stock_info['Close'].iloc[-1])), 3)

#     comp_data = (stock_data["mother_previous_high"] * 5) / 100
#     if stock_data["mother_previous_high"] - stock_data["mother_previous_low"] >= comp_data:
#         stock_data["high or low"] = 'High'
#     else:
#         stock_data["high or low"] = 'Low'
#     historical_info = stock.history(period="1y")
#     current_rsi = calculate_rsi(historical_info).iloc[-1]
#     stock_data["RSI"] = round(current_rsi, 2)
#     if current_rsi >  stock_data["mother_RSI"] :
#         stock_data["RSI Cross over"] = "RSI Cross - True"
#     else:
#         stock_data["RSI Cross over"] = "RSI Cross - False"

def color_text_rsi_comp(val):
    if val >= 75:
        return 'color: pink;'  # Change color to green for values > 100
    else:
        return 'color: green;' 

def color_text_comp(vals):
    return ['color: green' if val > s else 'color: pink' for val, s in zip(vals, stock_list_df['mother_previous_high'])]

def color_text_comp_low(vals):
    return ['color: blue' if val > s else 'color: pink' for val, s in zip(vals, stock_list_df['mother_previous_low'])]

def color_text_RR(val):
    if val == "RR - True":
        return 'color: green;'  # Change color to green for values > 100
    if val == "RR - False":
        return 'color: Pink;'

def color_text_price(val):
    if val == "Price - True":
        return 'color: green;'  # Change color to green for values > 100
    if val == "Price - False":
        return 'color: Pink;'
    
def color_text_rsi(val):
    if val == "RSI Cross - True":
        return 'color: green;'  # Change color to green for values > 100
    if val == "RSI Cross - False":
        return 'color: Pink;'
    
def color_text_rsi_cross(val):
    if val =="Price - True":
        return 'color: green;'  # Change color to green for values > 100
    if val =="Price - False":
        return 'color: Pink;'

def color_text(val):
    if val == True:
        return 'color: green;'  # Change color to green for values > 100
    else:
        return 'color: Pink;'
    
def color_text_value(val):
    if val == "Low":
        return 'color: green;'  # Change color to green for values > 100
    if val == "High":
        return 'color: Pink;'

def get_screener_condition_col(stock_data):
    stock = yf.Ticker(stock_data["Symbol"] + ".NS")
    print(f"Conditionl formation started for - {stock}")
    stock_info = stock.history(period="1d", interval="1m")  # 1-minute interval for near real-time
    stock_data["Price"] = round((float(stock_info['Close'].iloc[-1])), 3)
    comp_data = (stock_data["mother_previous_high"] * 5) / 100
    if stock_data["mother_previous_high"] - stock_data["mother_previous_low"] >= comp_data:
        stock_data["high or low"] = 'High'
    else:
        stock_data["high or low"] = 'Low'
    historical_info = stock.history(period="1y")
    current_rsi = calculate_rsi(historical_info).iloc[-1]
    stock_data["RSI"] = round(current_rsi, 2)
    if current_rsi >  stock_data["mother_RSI"] :
        stock_data["RSI Cross over"] = "RSI Cross - True"
    else:
        stock_data["RSI Cross over"] = "RSI Cross - False"
    actual_target =  round((stock_data["mother_previous_high"] + (2 * stock_data["mother_previous_high"] - stock_data["mother_previous_low"])), 2)
    five_per = (float(stock_info['Close'].iloc[-1]) * 105) / 100
    # stock_data["five_percent_Target"] = round(real_price, 2)

    if actual_target > five_per:
        stock_data["Price Crossover"] = "Price - True"
    else:
        stock_data["Price Crossover"] = "Price - False"
    nine_five_of_real_price = (stock_info['Close'].iloc[-1] * 95) / 100
    if stock_data["mother_previous_low"] > nine_five_of_real_price:
        stock_data["RR Ratio"] = "RR - True"
    else:
        stock_data["RR Ratio"] = "RR - False"
    
    return stock_data




if __name__ == "__main__":
    while True:
        stock_list = pd.read_excel("stock_list/sheet2.xlsx").to_dict("records")
        for item in stock_list:
            get_screener_condition_col(stock_data = item)   
        stock_list_df = pd.DataFrame(stock_list)
        stock_list_df_styler = (
            stock_list_df.style
            .map(color_text_value, subset=['high or low'])
            .map(color_text_rsi, subset=['RSI Cross over'])
            .map(color_text_rsi_cross, subset=['Price Crossover'])
            .map(color_text_RR, subset=['RR Ratio'])
            .map(color_text_rsi_comp, subset=['RSI'])
            .map(color_text_resistance, subset=['Resistance'])
            .map(color_text_nifty_trend, subset=['Nifty_Trend'])
            .map(color_text_sector_trend, subset=['Sector_Trend'])
            .apply(color_text_comp, subset=['Price'])
            .apply(color_text_comp_low, subset=['Price'])
        )
        try:
            stock_list_df_styler.to_excel('stock_list/sheet2.xlsx', engine='xlsxwriter', index=False)
            print("File saved successfully.")
        except PermissionError:
            print(f"File is in use. Retrying in 20 seconds...")
            time.sleep(20)
        except Exception:
            print("Haven't added trend infos...Please open excel and add the trend columns and try again")
            break
        stock_list_df_styler = stock_list_df_styler.hide(axis='columns', subset=['mother_previous_high', 'mother_previous_low'])
        html = stock_list_df_styler.to_html()

        # write html to file
        text_file = open("index.html", "w")
        text_file.write(html)
        text_file.close()
        print("Process Completed .... Live Price will be updated after 1 minute")
        time.sleep(60)

