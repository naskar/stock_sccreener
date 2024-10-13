import pandas as pd
import yfinance as yf

from mother_baby_filter import calculate_rsi
import time

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
    screener_stock_details = {}
    screener_stock_details["Company Name"]  = stock_data["Company Name"]
    screener_stock_details["Industry"]  = stock_data["Industry"]
    screener_stock_details["Symbol"]  = stock_data["Symbol"]
    screener_stock_details["mother_previous_high"]  = stock_data["mother_previous_high"]

    stock_info = stock.history(period="1d", interval="1m")  # 1-minute interval for near real-time
    screener_stock_details["Price"] = round((float(stock_info['Close'].iloc[-1])), 2)
    comp_data = (stock_data["mother_previous_high"] * 5) / 100
    if stock_data["mother_previous_high"] - stock_data["mother_previous_low"] >= comp_data:
        screener_stock_details["high or low"] = 'High'
    else:
        screener_stock_details["high or low"] = 'Low'
    historical_info = stock.history(period="1y")
    current_rsi = calculate_rsi(historical_info).iloc[-1]
    screener_stock_details["RSI"] = round(current_rsi, 2)
    if current_rsi >  stock_data["mother_RSI"] :
        screener_stock_details["RSI Cross over"] = "RSI Cross - True"
    else:
        screener_stock_details["RSI Cross over"] = "RSI Cross - False"
    actual_target =  round((stock_data["mother_previous_high"] + (2 * stock_data["mother_previous_high"] - stock_data["mother_previous_low"])), 2)
    five_per = (float(stock_info['Close'].iloc[-1]) * 105) / 100
    # screener_stock_details["five_percent_Target"] = round(real_price, 2)

    if actual_target > five_per:
        screener_stock_details["Price Crossover"] = "Price - True"
    else:
        screener_stock_details["Price Crossover"] = "Price - False"
    nine_five_of_real_price = (stock_info['Close'].iloc[-1] * 95) / 100
    if stock_data["mother_previous_low"] > nine_five_of_real_price:
        screener_stock_details["RR Ratio"] = "RR - True"
    else:
        screener_stock_details["RR Ratio"] = "RR - False"
    
    return screener_stock_details




if __name__ == "__main__":
    stock_list = []
    stock_list_1 =pd.read_excel("stock_list/mother_baby_stock.xlsx").to_dict(orient="records")
    stock_list_2 = pd.read_excel("stock_list/sheet2.xlsx").to_dict("records")
    for i in range(len(stock_list_2)):
        for j in range(len(stock_list_1)):
            if stock_list_2[i]["Symbol"] == stock_list_1[j]["Symbol"]:
                stock_list.append(stock_list_1[j])
    while True:
        stock_data_list = []
        try:
            for item in stock_list:
                stock_data_list.append(get_screener_condition_col(stock_data = item))
        except Exception as e:
            print(e)


        stock_list_df = pd.DataFrame(stock_data_list)
        stock_list_df_styler = (
            stock_list_df.style
            .map(color_text_rsi, subset=['RSI'])
            .map(color_text_value, subset=['high or low'])
            .map(color_text_rsi, subset=['RSI Cross over'])
            .map(color_text_rsi_cross, subset=['Price Crossover'])
            .map(color_text_RR, subset=['RR Ratio'])
        )
        html = stock_list_df_styler.to_html()

        # write html to file
        text_file = open("index.html", "w")
        text_file.write(html)
        text_file.close()
        print("Process Completed .... Price will be updated after 1 minute")
        time.sleep(60)