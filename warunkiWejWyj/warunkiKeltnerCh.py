import MetaTrader5 as mt5
import time
import datetime
import pandas_ta as ta

from wskazniki.keltner import calculate_keltner_channels as keltnerChannels
from wskazniki.tema import tema
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

    # obliczanie kanału Keltnera
    keltChan = keltnerChannels(df, length=40, multiplier=2)

    # obliczanie EMA
    df['ema'] = tema(df['Close'], 8)

    #obliczanie ostatnich wartości
    last_close = df['Close'].iloc[-2]
    last_ema = df['ema'].iloc[-2]
    last_lower_band = keltChan['KCLe_40_2.0'].iloc[-2]
    last_upper_band = keltChan['KCUe_40_2.0'].iloc[-2]
    last_middle_band = keltChan['KCBe_40_2.0'].iloc[-2]

    if (long_position is None):
        prev_ema = df['ema'].iloc[-3]
        prev_upper_band = keltChan['KCUe_40_2.0'].iloc[-3]
        if datetime.datetime.now().hour < 21 and datetime.datetime.now().hour > 7:
            if datetime.datetime.now().hour == 20 and datetime.datetime.now().minute >= 50:
                close_all_positions(symbol)
                return
            if prev_ema < prev_upper_band and last_ema > last_upper_band:
                # otwarcie pozycji długiej
                print(f'Otwieranie pozycji dlugiej dla {symbol} o godzinie {time.strftime("%H:%M:%S", time.localtime())}')
                open_long_position_with_sl_tp(symbol, 0.1, 1000, 9)
    else:
        if (last_close <= last_middle_band):
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


    # obliczanie kanału Keltnera
    keltChan = keltnerChannels(df, length=40, multiplier=2)

    # obliczanie EMA
    df['ema'] = tema(df['Close'], 8)

    #obliczanie ostatnich wartości
    last_close = df['Close'].iloc[-2]
    last_ema = df['ema'].iloc[-2]
    last_lower_band = keltChan['KCLe_40_2.0'].iloc[-2]
    last_upper_band = keltChan['KCUe_40_2.0'].iloc[-2]
    last_middle_band = keltChan['KCBe_40_2.0'].iloc[-2]
    
    if (short_position is None):
        prev_ema = df['ema'].iloc[-3]
        prev_lower_band = keltChan['KCLe_40_2.0'].iloc[-3]
        if datetime.datetime.now().hour < 21 and datetime.datetime.now().hour > 7:
            if datetime.datetime.now().hour == 20 and datetime.datetime.now().minute >= 50:
                close_all_positions(symbol)
                return
            if prev_ema > prev_lower_band and last_ema < last_lower_band:
                # otwarcie pozycji krótkiej
                print(f'Otwieranie pozycji krótkiej dla {symbol} o godzinie {time.strftime("%H:%M:%S", time.localtime())}')
                open_short_position_with_sl_tp(symbol, 0.1, 1000, 9)
    else:
        if last_close >= last_middle_band:
            # zamknięcie pozycji krótkiej
            print(f'Zamykanie pozycji krótkiej dla {symbol} o godzinie {time.strftime("%H:%M:%S", time.localtime())}')
            close_all_positions(symbol)