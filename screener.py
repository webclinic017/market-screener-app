#!/usr/bin/env python
# coding: utf-8

# # Confluence Signal

# ![image.png](attachment:image.png)
# 
# ![image-2.png](attachment:image-2.png)

# In[79]:


import numpy as np
import pandas as pd
import yfinance as yf
import datetime 
import ta
#import talib
import plotly
import plotly.express as px
import plotly.graph_objects as go

"""import MetaTrader5 as mt5
# connect to MetaTrader 5
if not mt5.initialize():
    print("initialize() failed")
    #mt5.shutdown()"""


# Calculate new parameters
from ta.trend import EMAIndicator
from ta.trend import SMAIndicator
from ta.volatility import AverageTrueRange
from ta.momentum import RSIIndicator
from ta.momentum import StochasticOscillator
from ta.trend import ADXIndicator
from ta.trend import CCIIndicator
from ta.trend import MACD
from ta.momentum import StochRSIIndicator
from ta.momentum import AwesomeOscillatorIndicator
from ta.momentum import williams_r
from ta.momentum import UltimateOscillator
from ta.momentum import ROCIndicator

get_ipython().run_line_magic('matplotlib', 'inline')


# In[95]:


"""def get_data(symbol, timeframe):

    df = mt5.copy_rates_from_pos(symbol, timeframe, 0, 500)
    #df = mt5.copy_rates_range(symbol, mt5.TIMEFRAME_H1, dt(2019,1,1,0), dt(2022,8,11,23))

    # create DataFrame out of the obtained data
    df = pd.DataFrame(df)
    # convert time in seconds into the datetime format
    df['time']=pd.to_datetime(df['time'], unit='s')
    df.index = df.time.values
    df = df.drop(["time", "spread", "real_volume", "tick_volume"], axis = 1)
    df.columns = ["Open", "High", "Low", "Close"]
    
    df = df.dropna()
    return df"""


# get stock data
def get_data(symbol, timeframe):


    time_dic = {
    "1D" : 500,
    "1H" : 60,
    "30M" : 20,
   "15M" : 10,
    "5M" : 10,
    "1M" : 2
    }
    
    INTERVAL = timeframe     # Sample rate of historical data
    NUM_DAYS = time_dic[INTERVAL]  # The number of days of historical data to retrieve
    symbol = str(f"{symbol}=X")  #str(input("Please enter stock symbol: "))     # Symbol of the desired stock

    #define start & dates
    start = (datetime.date.today() - datetime.timedelta( NUM_DAYS ) )
    end = datetime.datetime.today()
    
    #pull data
    df = yf.download(symbol, start=start, end=end, interval = INTERVAL)
    df.drop(["Adj Close", "Volume"], axis = 1, inplace = True)
    df.index.name = "time"

    return df


# In[81]:


def add_indicators(df):

    #----------------------------------------------------------------
    #Exponential Moving Averages
    #----------------------------------------------------------------

    #ema5
    ema5 = EMAIndicator(close = df.Close, window = 5)
    df["ema5"] = round(ema5.ema_indicator(), 5)

    #ema10
    ema10 = EMAIndicator(close = df.Close, window = 10)
    df["ema10"] = round(ema10.ema_indicator(), 5)

    #ema20
    ema20 = EMAIndicator(close = df.Close, window = 20)
    df["ema20"] = round(ema20.ema_indicator(), 5)

    #ema30
    ema30 = EMAIndicator(close = df.Close, window = 30)
    df["ema30"] = round(ema30.ema_indicator(), 5)

    #ema50
    ema50 = EMAIndicator(close = df.Close, window = 50)
    df["ema50"] = round(ema50.ema_indicator(), 5)

    #ema100
    ema100 = EMAIndicator(close = df.Close, window = 100)
    df["ema100"] = round(ema100.ema_indicator(), 5)

    #ema200
    ema200 = EMAIndicator(close = df.Close, window = 200)
    df["ema200"] = round(ema200.ema_indicator(), 5)


    #----------------------------------------------------------------
    # Simple Moving Averages
    #----------------------------------------------------------------

    #sma5
    sma5 = SMAIndicator(close = df.Close, window = 5)
    df["sma5"] = round(sma5.sma_indicator(), 5)

    #sma10
    sma10 = SMAIndicator(close = df.Close, window = 10)
    df["sma10"] = round(sma10.sma_indicator(), 5)

    #sma20
    sma20 = SMAIndicator(close = df.Close, window = 20)
    df["sma20"] = round(sma20.sma_indicator(), 5)

    #sma30
    sma30 = SMAIndicator(close = df.Close, window = 30)
    df["sma30"] = round(sma30.sma_indicator(), 5)

    #sma50
    sma50 = SMAIndicator(close = df.Close, window = 50)
    df["sma50"] = round(sma50.sma_indicator(), 5)

    #sma100
    sma100 = SMAIndicator(close = df.Close, window = 100)
    df["sma100"] = round(sma100.sma_indicator(), 5)

    #sma200
    sma200 = SMAIndicator(close = df.Close, window = 200)
    df["sma200"] = round(sma200.sma_indicator(), 5)

    #----------------------------------------------------------------
    # Oscilators
    #----------------------------------------------------------------

    #rsi(14)
    rsi = RSIIndicator(close = df.Close, window = 14)
    df["rsi"] = round(rsi.rsi(), 5)

    #stoch(14,3)
    stoch = StochasticOscillator(df.High, df.Low, df.Close, window = 14, smooth_window = 3)
    df["stoch"] = round(stoch.stoch_signal(), 5)

    #adx(14)
    adx = ADXIndicator(df.High, df.Low, df.Close, window = 14)
    df["adx"] = round(adx.adx(), 5)

    #cci
    cci = CCIIndicator(df.High, df.Low, df.Close, window = 20)
    df["cci"] = round(cci.cci(), 5)

    """#momentum
    df["mom"] = talib.MOM(df.Close, timeperiod=10)"""

    #AO
    ao = AwesomeOscillatorIndicator(df.High, df.Low, window1 = 5, window2 = 34)
    df["ao"] = round(ao.awesome_oscillator(), 5)

    #stochrsi(14,3,3)
    stochrsi = StochRSIIndicator(df.Close, window = 14, smooth1 = 3, smooth2 = 3)
    df["stochrsi"] = round(stochrsi.stochrsi_k(), 5)

    #MACD(12,26)
    macd = MACD(df.Close)
    df["macd"] = round(macd.macd_diff(), 5)

    #WPR(14)
    wpr = williams_r(df.High, df.Low, df.Close)
    df["wpr"] = round(wpr, 5)

    #UO(14)
    uo = UltimateOscillator(df.High, df.Low, df.Close)
    df["uo"] = round(uo.ultimate_oscillator(), 5)

    df.dropna(inplace = True)
    return df


# In[82]:


def confluence(df):
    signal_buy = 0
    signal_sell = 0
    signal_neutral = 0
    
    indicators_list = ["EMA5", "EMA10", "EMA20", "EMA30", "EMA50", "EMA100", 
                      "SMA5", "SMA10", "SMA20", "SMA30", "SMA50", "SMA100",
                      "RSI(14)", "STOCH(14, 3, 3)", "CCI(20)", "ADX(14)", "MOM(10)", "AO",
                       "STOCHRSI(3, 3, 14)", "MACD(12,26)","WPR(14)", "ULTIMATE OSCILLATOR(7,14,28)"]
    
    indicator_signal = []
    
    #----------------------------------------------------------------
    #Exponential Moving Averages
    #----------------------------------------------------------------
    
    if df["ema5"][-1] < df["Close"][-1]:
        signal = "buy"
        signal_buy += 1
        
    elif df["ema5"][-1] > df["Close"][-1]:
        signal = "sell"
        signal_sell += 1
        
    else:
        signal = "neutral"
        signal_neutral += 1
        
    indicator_signal.append(signal)
        
    if df["ema10"][-1] < df["Close"][-1]:
        signal = "buy"
        signal_buy += 1
        
    elif df["ema10"][-1] > df["Close"][-1]:
        signal = "sell"
        signal_sell += 1
        
    else:
        signal = "neutral"
        signal_neutral += 1
        
    indicator_signal.append(signal)
        
    if df["ema20"][-1] < df["Close"][-1]:
        signal = "buy"
        signal_buy += 1
        
    elif df["ema20"][-1] > df["Close"][-1]:
        signal = "sell"
        signal_sell += 1
        
    else:
        signal = "neutral"
        signal_neutral += 1
        
    indicator_signal.append(signal)
        
    if df["ema30"][-1] < df["Close"][-1]:
        signal = "buy"
        signal_buy += 1
        
    elif df["ema30"][-1] > df["Close"][-1]:
        signal = "sell"
        signal_sell += 1
        
    else:
        signal = "neutral"
        signal_neutral += 1
        
    indicator_signal.append(signal)
        
    if df["ema50"][-1] < df["Close"][-1]:
        signal = "buy"
        signal_buy += 1
        
    elif df["ema50"][-1] > df["Close"][-1]:
        signal = "sell"
        signal_sell += 1
        
    else:
        signal = "neutral"
        signal_neutral += 1
        
    indicator_signal.append(signal)
        
    if df["ema100"][-1] < df["Close"][-1]:
        signal = "buy"
        signal_buy += 1
        
    elif df["ema100"][-1] > df["Close"][-1]:
        signal = "sell"
        signal_sell += 1
        
    else:
        signal = "neutral"
        signal_neutral += 1
        
    indicator_signal.append(signal)
        
    #----------------------------------------------------------------
    #Simple Moving Averages
    #----------------------------------------------------------------
    
    if df["sma5"][-1] < df["Close"][-1]:
        signal = "buy"
        signal_buy += 1
        
    elif df["sma5"][-1] > df["Close"][-1]:
        signal = "sell"
        signal_sell += 1
        
    else:
        signal = "neutral"
        signal_neutral += 1
        
    indicator_signal.append(signal)
        
    if df["sma10"][-1] < df["Close"][-1]:
        signal = "buy"
        signal_buy += 1
        
    elif df["sma10"][-1] > df["Close"][-1]:
        signal = "sell"
        signal_sell += 1
        
    else:
        signal = "neutral"
        signal_neutral += 1
        
    indicator_signal.append(signal)
        
    if df["sma20"][-1] < df["Close"][-1]:
        signal = "buy"
        signal_buy += 1
        
    elif df["sma20"][-1] > df["Close"][-1]:
        signal = "sell"
        signal_sell += 1
        
    else:
        signal = "neutral"
        signal_neutral += 1
        
    indicator_signal.append(signal)
        
    if df["sma30"][-1] < df["Close"][-1]:
        signal = "buy"
        signal_buy += 1
        
    elif df["sma30"][-1] > df["Close"][-1]:
        signal = "sell"
        signal_sell += 1
        
    else:
        signal == "Neutral"
        signal_neutral +=1 
        
    indicator_signal.append(signal)
        
    if df["sma50"][-1] < df["Close"][-1]:
        signal = "buy"
        signal_buy += 1
        
    elif df["sma50"][-1] > df["Close"][-1]:
        signal = "sell"
        signal_sell += 1
        
    else:
        signal = "neutral"
        signal_neutral += 1
        
    indicator_signal.append(signal)
        
    if df["sma100"][-1] < df["Close"][-1]:
        signal = "buy"
        signal_buy += 1
        
    elif df["sma100"][-1] > df["Close"][-1]:
        signal = "sell"
        signal_sell += 1
        
    else:
        signal = "neutral"
        signal_neutral += 1
        
    indicator_signal.append(signal)
        
    #----------------------------------------------------------------
    #Oscilators
    #----------------------------------------------------------------
    
    if df["rsi"][-1] > 70.0:
        signal = "buy"
        signal_buy += 1
        
    elif df["rsi"][-1] < 30.0:
        signal = "sell"
        signal_sell += 1
        
    else:
        signal = "neutral"
        signal_neutral += 1
        
    indicator_signal.append(signal)
        
    if df["stoch"][-1] > 80.0:
        signal = "buy"
        signal_buy += 1
        
    elif df["stoch"][-1] < 20.0:
        signal = "sell"
        signal_sell += 1
        
    else:
        signal = "neutral"
        signal_neutral += 1
        
    indicator_signal.append(signal)
        
    if df["cci"][-1] > 100.0:
        signal = "buy"
        signal_buy += 1
        
    elif df["cci"][-1] < -100.0:
        signal = "sell"
        signal_sell += 1
        
    else:
        signal = "neutral"
        signal_neutral += 1
        
    indicator_signal.append(signal)
        
    if df["adx"][-1] > 25.0:
        signal = "buy"
        signal_buy += 1
        
    elif df["adx"][-1] > 25.0:
        signal = "sell"
        signal_sell += 1
        
    else:
        signal = "neutral"
        signal_neutral += 1
        
    indicator_signal.append(signal)
            
    """if df["mom"][-1] > 0.0:
        signal = "buy"
        signal_buy += 1
        
    elif df["mom"][-1] < 0.0:
        signal = "sell"
        signal_sell += 1
        
    else:
        signal = "neutral"
        signal_neutral += 1
        
    indicator_signal.append(signal)"""
        
    if df["ao"][-1] > 0.0:
        signal = "buy"
        signal_buy += 1
        
    elif df["ao"][-1] < 0.0:
        signal = "sell"
        signal_sell += 1
        
    else:
        signal = "neutral"
        signal_neutral += 1
        
    indicator_signal.append(signal)
        
    if df["stochrsi"][-1] > 80.0:
        signal = "buy"
        signal_buy += 1
        
    elif df["stochrsi"][-1] < 20.0:
        signal = "sell"
        signal_sell += 1
        
    else:
        signal = "neutral"
        signal_neutral += 1
        
    indicator_signal.append(signal)
        
    if df["macd"][-1] > df["macd"][-2]:
        signal = "buy"
        signal_buy += 1
        
    elif df["macd"][-1] < df["macd"][-2]:
        signal = "sell"
        signal_sell += 1
        
    else:
        signal = "neutral"
        signal_neutral += 1
        
    indicator_signal.append(signal)
        
    if df["wpr"][-1] > -20.0:
        signal = "buy"
        signal_buy += 1
        
    elif df["wpr"][-1] < -80.0:
        signal = "sell"
        signal_sell += 1
        
    else:
        signal = "neutral"
        signal_neutral += 1
        
    indicator_signal.append(signal)
        
    if df["uo"][-1] > 70.0:
        signal = "buy"
        signal_buy += 1
        
    elif df["uo"][-1] < 30.0:
        signal = "sell"
        signal_sell += 1
        
    else:
        signal = "neutral"
        signal_neutral += 1
        
    indicator_signal.append(signal)
        
    #----------------------------------------------------------------
    #Confluence
    #----------------------------------------------------------------
    
    total_signals = sum([signal_buy, signal_sell, signal_neutral])

    perc_buy = round((signal_buy/total_signals) * 100, 1)
    perc_sell = round((signal_sell/total_signals) * 100, 1)
    perc_neutral = round((signal_neutral/total_signals) * 100, 1)

    #print(f"{perc_buy}% Buy, {perc_sell}% Sell, {perc_neutral}% Neutral")
    
    #----------------------------------------------------------------
    #Table
    #----------------------------------------------------------------
    
    table = pd.DataFrame([f"{perc_buy}%", f"{perc_sell}%", f"{perc_neutral}%"])
    table = table.T
    table.columns = ["Buy", "Sell", "Neutral"]
    #table
    
    if perc_buy > 75:
        con_signal = "Strong Buy"
    
    elif perc_buy > 49 < 75:
        con_signal = "Buy"

    elif perc_sell > 75:
        con_signal = "Strong Sell"

    elif perc_sell > 49 < 75:
        con_signal = "Sell"

    elif perc_neutral > 49 or (perc_buy < 50 and perc_sell < 50):
        con_signal = "Neutral"

    #print(con_signal)
    

        
    return con_signal


# In[85]:


def screener():

    symbols = ["EURUSD", "AUDUSD", "USDCAD", "USDCHF", "AUDCAD", "CADCHF", "NZDUSD", "EURCAD", "AUDCHF", 
                          "GBPUSD", "GBPCAD", "GBPNZD", "AUDNZD", "EURGBP", "EURNZD", "GBPCHF", "EURCHF", "EURAUD", 
                          "NZDCAD", "NZDCHF", "GBPAUD", "GBPJPY", 
                          "CADJPY", "EURJPY", "AUDJPY", "NZDJPY","USDJPY","CHFJPY"]

    time_frame = "1D" #mt5.TIMEFRAME_D1
    signals = []
    dataset = []
    final_data = []

    for symbol in symbols:
        df = get_data(symbol, time_frame)
        df["%change"] = round(df['Close'].pct_change(), 4)*100
        dataset. append(df)

        data = add_indicators(df.copy())
        conf = confluence(data)
        signals.append(conf)


    for symbol, df, signal in zip(symbols, dataset, signals):
        dff = pd.DataFrame(df.iloc[-1]).T
        dff.index = [symbol]
        dff["Rating"] = signal
        final_data.append(dff)

    table = pd.concat(final_data)
    table.reset_index(inplace = True)
    table = table.rename(columns = {"index":"Currency Pairs"})
    #table[["Open", "High", "Low", "Close"]].round(decimals = 5)
    table = table.rename(columns = {"index":"Currency Pairs", "Close" : "Price"})
    
    pct = []
    open_ = []
    high = []
    low = []
    price = []

    for i in table["%change"]:
        i = round(i, 3)
        i = f"{i}%"
        pct.append(i)

    for i in table["Open"]:
        i = round(i, 5)
        open_.append(i)

    for i in table["High"]:
        i = round(i, 5)
        high.append(i)

    for i in table["Low"]:
        i = round(i, 5)
        low.append(i)

    for i in table["Price"]:
        i = round(i, 5)
        price.append(i)


    table["%change"] = pct
    table["Open"] = open_
    table["High"] = high
    table["Low"] = low
    table["Price"] = price
    
    return table
    
    
    return table
    


screener()


# In[ ]:




