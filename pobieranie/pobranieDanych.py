import MetaTrader5 as mt5
import pandas as pd
import time

def PobranieDanych(symbol = 'EURUSD.pro', timeframe = mt5.TIMEFRAME_H1, start = 0, end = 1000):
    try:
        # pobranie danych z MT5
        candles = mt5.copy_rates_from_pos(symbol, timeframe, start, end)

        # zapisanie danych do DataFrame
        df = pd.DataFrame(candles)

        df.rename(columns={'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'tick_volume': 'Volume'}, inplace=True)

        # Expect data.index as DatetimeIndex
        df['Date'] = pd.to_datetime(df['time'], unit='s')
        df.set_index('Date', inplace=True)

    except Exception as e:
        print(f"An error occurred while downloading price history: {e} at {time.strftime('%H:%M:%S', time.localtime())}")

    return df

