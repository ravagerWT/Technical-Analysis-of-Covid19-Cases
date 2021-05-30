import pandas as pd
import numpy as np
from typing import Type, Tuple, List


# define MACD indicator calculation as function
# Read more: Moving Average Convergence Divergence (MACD) https://www.investopedia.com/terms/m/macd.asp#ixzz5VfwX1yUA
# default MACD period values are: period_long = 26, period_short = 12, period_singal = 9.
def calculate_macd(df, PRICE_NAME: str, period_long: int = 26, period_short: int = 12, period_singal: int = 9):
    EMA_long = df[PRICE_NAME].ewm(span=period_long, adjust=False).mean()
    EMA_short = df[PRICE_NAME].ewm(span=period_short, adjust=False).mean()
    MACD_line = EMA_short - EMA_long
    MACD_Signal_line = MACD_line.ewm(span=period_singal, adjust=False).mean()
    MACD_Histogram = MACD_line - MACD_Signal_line
    return MACD_line, MACD_Signal_line, MACD_Histogram

# Calculating RSI indicator  # ref:https://stackoverflow.com/questions/40181344/how-to-annotate-types-of-multiple-return-values
def calculate_rsi(df: Type[pd.DataFrame], price_name: str = 'daily_cases', rsi_length: int = 14) -> Tuple[Type[pd.Series], List]:
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
    return rsi_series, rsi_series.tolist()