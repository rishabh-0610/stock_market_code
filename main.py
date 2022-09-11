# This is a sample Python script.
# E1HA8Y7PIF1HD8AZ

import yfinance as yf
import pandas as pd
import requests
import constants
import datetime as dt


def main_function():
    ohlc_complete_data = get_ohlc_data('INFY.BSE')

    bullish_current_candle = is_bullish_candle(ohlc_complete_data[0], ohlc_complete_data[3])
    bullish_prev_candle = is_bullish_candle(ohlc_complete_data[4], ohlc_complete_data[7])

    if is_it_bullish_engulfing(ohlc_complete_data, bullish_current_candle, bullish_prev_candle):



def is_it_bullish_engulfing(ohlc_data, current_bullish, prev_bullish):
    if current_bullish:
        return [ohlc_data[0] < ohlc_data[4] and ohlc_data[3] > ohlc_data[7], prev_bullish]


def is_bullish_candle(openPrice, closePrice):
    return closePrice > openPrice


def get_ohlc_data(ticker):
    # global currentClose, currentLow, currentHigh, currentOpen, prevOpen, prevHigh, prevLow, prevClose, currentVolume
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + ticker + '&outputsize=fullsize&apikey=E1HA8Y7PIF1HD8AZ'
    r = requests.get(url)
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
