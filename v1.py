
# Imports
from pandas_datareader import data as pdr
from yahoo_fin import stock_info as si
from pandas import ExcelWriter
import yfinance as yf
import pandas as pd
import datetime
import time
yf.pdr_override()

#####################################################################################################################
#Choose between 2 markets

x = input('Tap 1 for the S&P500 or 2 for the Dow Jones ')

if (x == '1'):
    tickers = si.tickers_sp500()
    tickers = [item.replace(".", "-") for item in tickers] # Yahoo Finance uses dashes instead of dots
    index_name =  '^GSPC' # S&P 500
    start_date = datetime.datetime.now() - datetime.timedelta(days=365)
    end_date = datetime.date.today()
    exportList = pd.DataFrame(columns=['Stock', "RS_Rating", "50 Day MA", "150 Day Ma", "200 Day MA", "52 Week Low", "52 week High"])
    returns_multiples = []

if (x == '2'):
    tickers = si.tickers_dow()
    tickers = [item.replace(".", "-") for item in tickers] # Yahoo Finance uses dashes instead of dots
    index_name =  '^DJI' # S&P 500
    start_date = datetime.datetime.now() - datetime.timedelta(days=365)
    end_date = datetime.date.today()
    exportList = pd.DataFrame(columns=['Stock', "RS_Rating", "50 Day MA", "150 Day Ma", "200 Day MA", "52 Week Low", "52 week High"])
    returns_multiples = []
tickers
