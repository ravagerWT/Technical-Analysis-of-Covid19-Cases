import pandas as pd
import matplotlib
# matplotlib.use('TkAgg')  # show matplotlib graph window in front of other windows (for macOS)
import matplotlib.pyplot as plt
from typing import Type

from Covid19DataHandler import getCovidDataFrame


# define MACD indicator calculation as function

# How to understand this indicator
# 1. Crossovers - As shown in the chart above, when the MACD falls below the signal line, it is a bearish signal,
# which indicates that it may be time to sell. Conversely, when the MACD rises above the signal line,
# the indicator gives a bullish signal, which suggests that the price of the asset is likely to experience upward
# momentum. Many traders wait for a confirmed cross above the signal line before entering into a position to avoid
# getting "faked out" or entering into a position too early, as shown by the first arrow.
#
# 2. Divergence - When the security price diverges from the MACD, it signals the end of the current trend.
# For example, a stock price that is rising and a MACD indicator that is falling could mean that the rally
# is about to end. Conversely, if a stock price is falling and the MACD is rising, it could mean that a
# bullish reversal could occur in the near-term. Traders often use divergence in conjunction with other technical
# indicators to find opportunities.
#
# 3. Dramatic Rise - When the MACD rises dramatically - that is, the shorter moving average pulls away from the
# longer-term moving average - it is a signal that the security is overbought and will soon return to normal levels.
# Traders will often combine this analysis with the Relative Strength Index (RSI) or other technical indicators
# to verify overbought or oversold conditions.
#
# Traders also watch for a move above or below the zero line because this signals the position of the short-term
# average relative to the long-term average. When the MACD is above zero, the short-term average is above the
# long-term average, which signals upward momentum. The opposite is true when the MACD is below zero.
# As you can see from the chart above, the zero line often acts as an area of support and resistance for the indicator.
#
# Read more: Moving Average Convergence Divergence (MACD) https://www.investopedia.com/terms/m/macd.asp#ixzz5VfwX1yUA

# default MACD period values are: period_long = 26, period_short = 12, period_singal = 9.
def calculate_macd(df, PRICE_NAME, period_long, period_short, period_singal):
    EMA_long = df[PRICE_NAME].ewm(span=period_long, adjust=False).mean()
    EMA_short = df[PRICE_NAME].ewm(span=period_short, adjust=False).mean()
    MACD_line = EMA_short - EMA_long
    MACD_Signal_line = MACD_line.ewm(span=period_singal, adjust=False).mean()
    MACD_Histogram = MACD_line - MACD_Signal_line
    return MACD_line, MACD_Signal_line, MACD_Histogram


def renderMACDPlot(df: Type[pd.DataFrame], plot_title='MACD', ylabel='Quantity', timestamp_name = 'date', price_name = 'daily_cases'):
    ### 2. Show historic price data in the first subplot
    plt.figure(figsize=(10,5)) # change default figure size
    ax1 = plt.subplot(2, 1, 1)
    plt.plot(df[timestamp_name], df[price_name])
    plt.title(plot_title)
    plt.ylabel(ylabel)
    # plt.grid()

    frame1 = plt.gca() # hide x axis values
    frame1.axes.xaxis.set_ticklabels([])

    ### 3. Calculate MACD indicator and add it to subplot
    MACD_line, MACD_Signal_line, MACD_Histogram = calculate_macd(df, price_name, 26, 12, 9) # calculating with the default MACD values

    # add data to subplot
    ax2 = plt.subplot(2, 1, 2, sharex = ax1)
    plt.plot(df[timestamp_name], MACD_line, color = 'blue')
    plt.plot(df[timestamp_name], MACD_Signal_line, color = 'red')
    plt.bar(df[timestamp_name], MACD_Histogram)
    # plt.grid()

    frame1 = plt.gca() # hide x axis values
    frame1.axes.xaxis.set_ticklabels([])

    ### 4. Show subplot
    plt.show()

if __name__ == '__main__':
    data_path = 'time_series_covid19_confirmed_global.csv'
    df = getCovidDataFrame(data_path)
    renderMACDPlot(df,plot_title='Test')
