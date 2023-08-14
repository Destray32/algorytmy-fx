import MetaTrader5 as mt5
import pandas as pd

def PobranieDanych(symbol = 'EURUSD.pro', timeframe = mt5.TIMEFRAME_H1, start = 0, end = 1000):
    # pobranie danych z MT5
    candles = mt5.copy_rates_from_pos(symbol, timeframe, start, end)

    # zapisanie danych do DataFrame
    df = pd.DataFrame(candles)

    df.rename(columns={'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'tick_volume': 'Volume'}, inplace=True)

    # Expect data.index as DatetimeIndex
    df['Date'] = pd.to_datetime(df['time'], unit='s')
    df.set_index('Date', inplace=True)

    return df

