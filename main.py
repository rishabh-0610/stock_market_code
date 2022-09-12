# This is a sample Python script.
# E1HA8Y7PIF1HD8AZ

import requests
import constants
import whatsapp_api as telegram
import pandas as pd
import csv
import time as time


def main_function():
    with open('scrip_codes.csv', 'r') as file:
        file_content = csv.reader(file)
        index = 0
        stocks_in_bse = []
        for row in file_content:
            if index != 0 and index <= 100:
                stocks_in_bse.append(row[1])
            index = index + 1
    run_bse_stocks(stocks_in_bse)


def run_bse_stocks(needed_stocks):
    with open('BSE-A.csv', 'r') as file:
        file_content = csv.reader(file)
        index = 0
        for row in file_content:
            if index < 5:
                if row[0] in needed_stocks:
                    alpha_ticker = row[2] + ".BSE"
                    alpha_comp = row[1]
                    runner(alpha_ticker, alpha_comp)
                    index = index + 1
            else:
                index = 0
                telegram.send_message_to_bot("Bot is sleeping peacefully for 60 seconds because the API is lazy!!")
                time.sleep(60)



def runner(ticker_symbol, company_name):
    message = ""
    ohlc_complete_data = get_ohlc_data(ticker_symbol)
    if ohlc_complete_data:
        bullish_current_candle = is_bullish_candle(ohlc_complete_data[0], ohlc_complete_data[3])
        # bullish_prev_candle = is_bullish_candle(ohlc_complete_data[4], ohlc_complete_data[7])

        if is_it_bullish_engulfing(ohlc_complete_data, bullish_current_candle):
            message = message + "Stock : " + company_name + "\n"
            message = message + "Bullish Engulfing : TRUE\n"
            if ohlc_complete_data[8]:
                message = message + "Good Volume : TRUE"
            else:
                message = message + "Good Volume : FALSE"

        if message != "":
            telegram.send_message_to_bot(message)
        else:
            telegram.send_message_to_bot("Dummy Update for " + company_name)


def is_it_bullish_engulfing(ohlc_data, current_bullish):
    if current_bullish:
        return ohlc_data[0] < ohlc_data[4] and ohlc_data[3] > ohlc_data[7]


def is_bullish_candle(openPrice, closePrice):
    return closePrice > openPrice


def get_ohlc_data(ticker):
    # global currentClose, currentLow, currentHigh, currentOpen, prevOpen, prevHigh, prevLow, prevClose, currentVolume
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + ticker + '&outputsize=fullsize&apikey=E1HA8Y7PIF1HD8AZ'
    r = requests.get(url)
    if r.text.find("Error") != -1:
        return []
    else:
        stock_data = r.json()[constants.TIME_SERIES_DAILY]
        volume_sum = 0
        index = 0
        for value_date, value in list(stock_data.items())[:5]:
            volume_sum = volume_sum + int(value[constants.VOLUME])
            # print("Date : {0}, Stock Data : {1}".format(value_date, value))
            if index == 0:
                currentVolume = float(value[constants.VOLUME])
                currentOpen = float(value[constants.OPEN])
                currentHigh = float(value[constants.HIGH])
                currentLow = float(value[constants.LOW])
                currentClose = float(value[constants.CLOSE])
            if index == 1:
                prevOpen = float(value[constants.OPEN])
                prevHigh = float(value[constants.HIGH])
                prevLow = float(value[constants.LOW])
                prevClose = float(value[constants.CLOSE])
            index = index + 1
        averageVolume = float(volume_sum / 5)

        return [currentOpen, currentHigh, currentLow, currentClose, prevOpen, prevHigh, prevLow, prevClose,
                currentVolume > averageVolume]


main_function()
