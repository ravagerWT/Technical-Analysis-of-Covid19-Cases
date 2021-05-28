import pandas as pd
import matplotlib
import numpy as np
import matplotlib.pyplot as plt

from typing import List, Type

from Covid19DataHandler import getCovidDataFrame

# Calculating RSI indicator
def calculate_rsi(df: Type[pd.DataFrame], price_name: str = 'daily_cases', rsi_length: int = 14) -> List:
    ### How to understand this indicator
    # Wilder recommended using 70 and 30 as overbought and oversold levels respectively. Generally,
    # if the RSI rises above 30 it is considered bullish for the underlying stock. Conversely,
    # if the RSI falls below 70, it is a bearish signal. Some traders identify the long-term t
    # rend and then use extreme readings for entry points. If the long-term trend is bullish,
    # then oversold readings could mark potential entry points.

    Close = df[price_name]
    Chg = Close - Close.shift(1)
    Chg_pos = pd.Series(index=Chg.index, data=Chg[Chg>0])
    Chg_pos = Chg_pos.fillna(0)
    Chg_neg = pd.Series(index=Chg.index, data=-Chg[Chg<0])
    Chg_neg = Chg_neg.fillna(0)
    
    up_mean = []
    down_mean = []
    for i in range(rsi_length+1, len(Chg_pos)+1):
        up_mean.append(np.mean(Chg_pos.values[i-rsi_length:i]))
        down_mean.append(np.mean(Chg_neg.values[i-rsi_length:i]))

    # calculate RSI
    rsi = []
    for i in range(len(up_mean)):
        rsi.append(100 * up_mean[i] / (up_mean[i] + down_mean[i]))
    rsi_series = pd.Series(index=Close.index[rsi_length:], data=rsi)
    return rsi_series.tolist()

def renderRSIPlot(df: Type[pd.DataFrame], plot_title='RSI', ylabel='value', timestamp_name = 'date', price_name = 'daily_cases'):
    # Show historic price data in first subplot
    plt.figure(figsize=(10,5)) # change default figure size
    ax1 = plt.subplot(2, 1, 1)
    plt.plot(df[timestamp_name], df[price_name])
    plt.title(plot_title)
    plt.ylabel(ylabel)
    # plt.grid()

    frame1 = plt.gca() # hide x axis values
    frame1.axes.xaxis.set_ticklabels([])

    rsi = calculate_rsi(df)
    # add data to another subplot
    x2 = plt.subplot(2, 1, 2, sharex = ax1)
    plt.plot(rsi, color = 'blue')
    # plt.grid()

    # Show subplot
    plt.show()

if __name__ == '__main__':
    data_path = 'time_series_covid19_confirmed_global.csv'
    df = getCovidDataFrame(data_path)
    renderRSIPlot(df,plot_title='Test')
