#!/usr/bin/env python
# coding: utf-8

# In[2]:


# Imports
from pandas_datareader import data as pdr
from yahoo_fin import stock_info as si
from pandas import ExcelWriter
import yfinance as yf
import pandas as pd
import datetime
import time
yf.pdr_override()


# In[3]:


# Variables and user inputs

# Let user choose the index he wants to screen

choice = int(input("Tap 1 for Dowjones, Tap 2 for Nasdaq, Tap 3 for S&P 500: "))

if choice == 1:
    tickers = si.tickers_dow()
    tickers = [item.replace(".", "-") for item in tickers]
    index_name = '^DJI'
    start_date = datetime.datetime.now() - datetime.timedelta(days=365) #define start date as today - 1 year
    end_date = datetime.date.today() #define end date as todays date
    exportList = pd.DataFrame(columns=['Stock', "RS_Rating", "50 Day MA", "150 Day Ma", "200 Day MA", "52 Week Low", "52 week High", "PE-Ratio"])#define export list with column titels
    returns_multiples = [] #create empty list
    
if choice == 2:
    tickers = si.tickers_nasdaq()
    tickers = [item.replace(".", "-") for item in tickers]
    index_name = '^IXIC'
    start_date = datetime.datetime.now() - datetime.timedelta(days=365) #define start date as today - 1 year
    end_date = datetime.date.today() #define end date as todays date
    exportList = pd.DataFrame(columns=['Stock', "RS_Rating", "50 Day MA", "150 Day Ma", "200 Day MA", "52 Week Low", "52 week High", "PE-Ratio"])#define export list with column titels
    returns_multiples = [] #create empty list
    
elif choice == 3:
    tickers = si.tickers_sp500()
    tickers = [item.replace(".", "-") for item in tickers] # Yahoo Finance uses dashes instead of dots
    index_name = '^GSPC' # define indexname (dowjones)
    start_date = datetime.datetime.now() - datetime.timedelta(days=365) #define start date as today - 1 year
    end_date = datetime.date.today() #define end date as todays date
    exportList = pd.DataFrame(columns=['Stock', "RS_Rating", "50 Day MA", "150 Day Ma", "200 Day MA", "52 Week Low", "52 week High", "PE-Ratio"])#define export list with column titels
    returns_multiples = [] #create empty list


# In[4]:


# Index Returns
index_df = pdr.get_data_yahoo(index_name, start_date, end_date)
index_df['Percent Change'] = index_df['Adj Close'].pct_change() #add new col. (percent change) which is adjusted close pct change


# In[ ]:


index_return = (index_df['Percent Change'] +1).cumprod()[-1] #calculate cumulative index return -> last return is yoy return


# In[ ]:


# Find top 30% performing stocks (relative to the index)
for ticker in tickers:
    # Download historical data as CSV for each stock (makes the process faster)
    df = pdr.get_data_yahoo(ticker, start_date, end_date) #get for each ticker in the index, the data and store it in df
    df.to_csv(f'{ticker}.csv') #convert df into a csv

    # Calculating returns relative to the market (returns multiple)
    df['Percent Change'] = df['Adj Close'].pct_change() #add col. percentage change to dataframe (= adjst. cl. pct, change)
    stock_return = (df['Percent Change'] + 1).cumprod()[-1] #calculate cum. total return of the stock
    
    returns_multiple = round((stock_return / index_return), 2) # calculate the return relative to the index and round 2 decimales
    returns_multiples.extend([returns_multiple]) #extend the empty returns_multiples list created at the beginning
    
    print (f'Ticker: {ticker}; Returns Multiple against S&P 500: {returns_multiple}\n') 


# In[5]:


# get list of Dow tickers
 
 
 
# Get data in the current column for each stock's valuation table
dow_stats = {}
for ticker in tickers:
    try:
        temp = si.get_stats_valuation(ticker)
    except IndexError as e:
        print(f'{ticker}: {e}')  # print the ticker and the error
    print('\n')
    temp = temp.iloc[:,:2]
    temp.columns = ["Attribute", "Recent"]
    dow_stats[ticker] = temp
    
    
    


# In[14]:


combined_stats = pd.concat(dow_stats)
combined_stats = combined_stats.reset_index()
combined_stats


# In[15]:


del combined_stats["level_1"]
# update column names
combined_stats.columns = ["Ticker", "Attribute", "Recent"]
combined_stats


# In[22]:


pe_ratios = combined_stats[combined_stats["Attribute"]=="Trailing P/E"].reset_index


# In[23]:



    

