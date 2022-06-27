#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Imports
from pandas_datareader import data as pdr
from yahoo_fin import stock_info as si
from pandas import ExcelWriter
import yfinance as yf
import pandas as pd
import datetime
import time
yf.pdr_override()


# In[2]:


# Variables and user inputs

# Let user choose the index he wants to screen

choice = int(input("Type 1 for Dowjones, 2 for Nasdaq, or 3 for S&P 500: "))

if choice == 1:
    tickers = si.tickers_dow()
    tickers = [item.replace(".", "-") for item in tickers]
    index_name = '^DJI'
    start_date = datetime.datetime.now() - datetime.timedelta(days=365) #define start date as today - 1 year
    end_date = datetime.date.today() #define end date as todays date
    exportList = pd.DataFrame(columns=['Stock', "RS_Rating", "50 Day MA", "150 Day Ma", "200 Day MA", "52 Week Low", "52 week High", "PE-Ratio", "PEG-Ratio"])#define export list with column titels
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


# In[3]:


# Index Returns
index_df = pdr.get_data_yahoo(index_name, start_date, end_date)
index_df['Percent Change'] = index_df['Adj Close'].pct_change() #add new col. (percent change) which is adjusted close pct change


# In[4]:


index_return = (index_df['Percent Change'] +1).cumprod()[-1] #calculate cumulative index return -> last return is yoy return


# In[5]:


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


# In[6]:


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
    
    
    


# In[7]:


combined_stats = pd.concat(dow_stats)
combined_stats = combined_stats.reset_index()
combined_stats


# In[8]:


del combined_stats["level_1"]
# update column names
combined_stats.columns = ["Ticker", "Attribute", "Recent"]
combined_stats


# In[44]:


pe_ratios = combined_stats[combined_stats["Attribute"]=="Trailing P/E"]
pe_dict = dict(zip(pe_ratios.Ticker, pe_ratios.Recent))


# In[47]:


peg_ratios = combined_stats[combined_stats["Attribute"]=="PEG Ratio (5 yr expected)"]
peg_dict = dict(zip(peg_ratios.Ticker, peg_ratios.Recent))


# In[52]:


# Creating dataframe of only top 30%
rs_df = pd.DataFrame( #creats a pandas data frame
    list(zip(tickers, returns_multiples)), #list zip function merge three lists and creat  a list of tuples
    columns=['Ticker', 'Returns_multiple'])# add columns titel to pandas dataframe

rs_df['PE_Ratio']= rs_df['Ticker'].map(pe_dict)

rs_df["PEG_Ratio"] = rs_df["Ticker"].map(peg_dict)

#add RS_Rating column to dataframe
rs_df['RS_Rating'] = rs_df.Returns_multiple.rank(pct=True) * 100 # rank rs, pct = true -> normalize the ranks and assign a percent to the rank putting them all between 0-1, times by 100
rs_df = rs_df[rs_df.RS_Rating >= rs_df.RS_Rating.quantile(0.7)] # only take stocks in the to X% into dataframe

rs_df


# In[53]:


rs_stocks = rs_df['Ticker']
for stock in rs_stocks:    
    try:
        df = pd.read_csv(f'{stock}.csv', index_col=0)
        sma = [50, 150, 200]
        for x in sma:
            df["SMA_"+str(x)] = round(df['Adj Close'].rolling(window=x).mean(), 2)
        
        # Storing required values 
        currentClose = df["Adj Close"][-1]
        moving_average_50 = df["SMA_50"][-1]
        moving_average_150 = df["SMA_150"][-1]
        moving_average_200 = df["SMA_200"][-1]
        low_of_52week = round(min(df["Low"][-260:]), 2)
        high_of_52week = round(max(df["High"][-260:]), 2)
        RS_Rating = round(rs_df[rs_df['Ticker']==stock].RS_Rating.tolist()[0])
        PE_Ratio = rs_df[rs_df["Ticker"]== stock].PE_Ratio.tolist()[0]
        PEG_Ratio = rs_df[rs_df["Ticker"]== stock].PEG_Ratio.tolist()[0]
        
        
        try:
            moving_average_200_20 = df["SMA_200"][-20]
        except Exception:
            moving_average_200_20 = 0
            
        # Condition 1: Current Price > 150 SMA and > 200 SMA
        condition_1 = currentClose > moving_average_150 > moving_average_200
        
        # Condition 2: 150 SMA and > 200 SMA
        condition_2 = moving_average_150 > moving_average_200

        # Condition 3: 200 SMA trending up for at least 1 month
        condition_3 = moving_average_200 > moving_average_200_20
        
        # Condition 4: 50 SMA> 150 SMA and 50 SMA> 200 SMA
        condition_4 = moving_average_50 > moving_average_150 > moving_average_200
           
        # Condition 5: Current Price > 50 SMA
        condition_5 = currentClose > moving_average_50
           
        # Condition 6: Current Price is at least 30% above 52 week low
        condition_6 = currentClose >= (1.3*low_of_52week)
           
        # Condition 7: Current Price is within 25% of 52 week high
        condition_7 = currentClose >= (0.5*high_of_52week)
        
        # Condition 8: PE Ratio
        condition_8 = float(PE_Ratio) < 20
        
        # Condition 9: PEG Raio
        condition_9 = float(PEG_Ratio) < 4
        
        # If all conditions above are true, add stock to exportList
        if(condition_8 and condition_9):
            exportList = exportList.append({'Stock': stock, "RS_Rating": RS_Rating ,"50 Day MA": moving_average_50, "150 Day Ma": moving_average_150, "200 Day MA": moving_average_200, "52 Week Low": low_of_52week, "52 week High": high_of_52week, "PE-Ratio": PE_Ratio, "PEG-Ratio": PEG_Ratio }, ignore_index=True)
                      
    except Exception as e:
        print (e)
         


exportList

