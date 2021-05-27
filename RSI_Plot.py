import pandas as pd
import matplotlib
# matplotlib.use('TkAgg')  # show matplotlib graph window in front of other windows (for macOS)
import matplotlib.pyplot as plt

from typing import Type

from Covid19DataHandler import getCovidDataFrame

# Calculating RSI indicator
def calculate_rsi(df, price_name = 'daily_cases', rsi_length = 14):
    ### How to understand this indicator
    # Wilder recommended using 70 and 30 as overbought and oversold levels respectively. Generally,
    # if the RSI rises above 30 it is considered bullish for the underlying stock. Conversely,
    # if the RSI falls below 70, it is a bearish signal. Some traders identify the long-term t
    # rend and then use extreme readings for entry points. If the long-term trend is bullish,
    # then oversold readings could mark potential entry points.

    next_df = df[price_name].shift(1)
    next_df[0] = 0 # change the very first array value from 'nan' to 0
    change = df[price_name] - next_df

    # gain and loss array:
    gain = []
    loss = []
    for i in change:
        if (i > 0):
            gain.append(i)
            loss.append(0)
        else:
            loss.append(i)
            gain.append(0)

    # fill first avg_gain and avg_loss with None for graph
    avg_gain = []
    avg_loss = []
    RSI = []
    for i in range(rsi_length):
        RSI.append(None)
        avg_gain.append(None)
        avg_loss.append(None)

    # calculate first_avg_gain and first_avg_loss, add them to avg_gain, avg_loss
    first_avg_gain =  sum(gain [1:rsi_length]) / rsi_length
    first_avg_loss = sum(loss [1:rsi_length]) / rsi_length

    avg_gain.append(first_avg_gain)
    avg_loss.append(first_avg_loss)

    # calculate all other avg_gains and avg_loss
    for i in range(rsi_length, df[price_name].size):
        temp_gain = (avg_gain[i] * (rsi_length - 1) + gain[i]) / rsi_length
        avg_gain.append(temp_gain)
        temp_loss = (avg_loss[i] * (rsi_length - 1) + loss[i]) / rsi_length
        avg_loss.append(temp_loss)

    # RSI calculations
    for i in range (rsi_length, df[price_name].size):
        RS = abs(avg_gain[i] / avg_loss[i])
        temp_RSI = 100 - (100 / (1 + RS))
        RSI.append(temp_RSI)
    return RSI

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