import MetaTrader5 as mt5
import time
import pandas_ta as ta

from wskazniki.boilinger import BollingerBands
from pozycja.long import open_long_position_with_sl_tp
from pozycja.short import open_short_position_with_sl_tp
from pozycja.close import close_all_positions

def open_long_position(df, symbol):
    # sprawdzenie, czy nie ma już otwartej pozycji długiej dla tej samej pary walutowej
    open_positions = mt5.positions_get(symbol=symbol)
    long_position = None
    for position in open_positions:
        if position.type == mt5.ORDER_TYPE_BUY:
            long_position = position
            break

    # obliczenie Bollinger Bands
    bands = BollingerBands(df, window=14, num_std=2)

    #obliczanie ADX
    adx = ta.adx(df['High'], df['Low'], df['Close'], length=14)


    # sprawdzenie warunku wejścia na pozycję długą
    last_close = df['Close'].iloc[-1]
    last_lower_band = bands['Lower Band'].iloc[-1]
    last_upper_band = bands['Upper Band'].iloc[-1]
    last_adx = adx['ADX_14'].iloc[-1]
    if long_position is None:
        if (last_close <= last_lower_band) and (last_adx < 32):
            # otwarcie pozycji długiej
            
            print(f'Otwieranie pozycji długiej dla {symbol} o godzinie {time.strftime("%H:%M:%S", time.localtime())}')
            open_long_position_with_sl_tp(symbol, 0.1, 5, 11)
    else:
        if (last_close >= last_upper_band):
            # zamknięcie pozycji długiej
            
            print(f'Zamykanie pozycji długiej dla {symbol} o godzinie {time.strftime("%H:%M:%S", time.localtime())}')
            close_all_positions(symbol)


def open_short_position(df, symbol):
    # sprawdzenie, czy nie ma już otwartej pozycji krótkiej dla tej samej pary walutowej
    open_positions = mt5.positions_get(symbol=symbol)
    short_position = None
    for position in open_positions:
        if position.type == mt5.ORDER_TYPE_SELL:
            short_position = position
            break

    # obliczenie Bollinger Bands
    bands = BollingerBands(df, window=14, num_std=2)

    #obliczanie ADX
    adx = ta.adx(df['High'], df['Low'], df['Close'], length=14)

    # sprawdzenie warunku wejścia na pozycję krótką
    last_close = df['Close'].iloc[-1]
    last_lower_band = bands['Lower Band'].iloc[-1]
    last_upper_band = bands['Upper Band'].iloc[-1]
    last_adx = adx['ADX_14'].iloc[-1]
    if short_position is None:
        if (last_close >= last_upper_band) and (last_adx < 32):
            # otwarcie pozycji krótkiej
            print(f'Otwieranie pozycji krótkiej dla {symbol} o godzinie {time.strftime("%H:%M:%S", time.localtime())}')
            open_short_position_with_sl_tp(symbol, 0.1, 5, 11)
    else:
        if last_close <= last_lower_band:
            # zamknięcie pozycji krótkiej
            print(f'Zamykanie pozycji krótkiej dla {symbol} o godzinie {time.strftime("%H:%M:%S", time.localtime())}')
            close_all_positions(symbol)