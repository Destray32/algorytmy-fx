import pandas as pd
import pandas_ta as ta

def calculate_keltner_channels(df, length=40, multiplier=2):
    kc = ta.kc(df['High'], df['Low'], df['Close'], length=length, scalar=multiplier)
    return kc
