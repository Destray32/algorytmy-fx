import MetaTrader5 as mt5
import time
import datetime
import pandas_ta as ta
import plotly.graph_objs as go

from pozycja.long import open_long_position_with_sl_tp
from pozycja.short import open_short_position_with_sl_tp
from pozycja.close import close_all_positions

def open_long_position(df, symbol):
    nie_doji = ['US10.pro', 'US100.pro', 'US30.pro', 'US500.pro']
    mt5.initialize()
    threshold = 0.03
    body_threshold = 0.15
    # sprawdzenie, czy nie ma już otwartej pozycji długiej dla tej samej pary walutowej
    open_positions = mt5.positions_get(symbol=symbol)
    long_position = None
    short_position = None
    for position in open_positions:
        if position.type == mt5.ORDER_TYPE_BUY:
            long_position = position
            break

    # Oblicz świeczki Heikin Ashi (poczatkowe)
    df['HA_Close'] = (df['Open'] + df['High'] + df['Low'] + df['Close']) / 4
    # df['HA_Open'] = (df['Open'].shift(1) + df['Close'].shift(1)) / 2
    df.loc[df.index[0], 'HA_Open'] = df.loc[df.index[0], 'Open'] # pierwsza świeczka HA_Open = Open
    df['HA_High'] = df[['High', 'HA_Open', 'HA_Close']].max(axis=1)
    df['HA_Low'] = df[['Low', 'HA_Open', 'HA_Close']].min(axis=1)

    # oblicz świeczki Heikin Ashi (od polowy)
    for i in range(1, len(df)):
        df.loc[df.index[i], 'HA_Open'] = (df.loc[df.index[i-1], 'HA_Open'] + df.loc[df.index[i-1], 'HA_Close']) / 2

    # popraw świeczki Heikin Ashi
    df['HA_High'] = df[['High', 'HA_Open', 'HA_Close']].max(axis=1)
    df['HA_Low'] = df[['Low', 'HA_Open', 'HA_Close']].min(axis=1)

    # Znajdź świeczki "doji"
    df['doji'] = (abs(df['HA_Close'] - df['HA_Open']) / df['HA_Close']) * 100 < threshold

    # Znajdź świeczki spełniające kryteria
    df['criteria'] = False
    prev_doji = False
    for i, row in df.iterrows():
        if prev_doji and prev_candle is not None:
            body_size_current = abs(row['HA_Close'] - row['HA_Open'])
            body_size_prev = abs(prev_candle['HA_Close'] - prev_candle['HA_Open'])
            if (prev_candle['HA_Close'] > prev_candle['HA_Open']) and (prev_candle['HA_High'] > prev_candle['HA_Close']) and (prev_candle['HA_Low'] < prev_candle['HA_Open']) and (row['HA_Close'] > row['HA_Open']) and (row['HA_Low'] == row['HA_Open']) and (body_size_prev > body_threshold):
                df.loc[i, 'criteria_buy'] = True
            elif (row['HA_Close'] > row['HA_Open']) and (row['HA_Low'] == row['HA_Open']) and (body_size_current > body_threshold):
                df.loc[i, 'criteria'] = True
        prev_doji = row['doji']
        prev_candle = row

    # Oblicz EMA dla świeczek Heikin Ashi (długość 30 podczas pierwszego testu)
    df['HA_Close_EMA'] = ta.ema(df['HA_Close'], length=35)

    # sprawdz ile zer po przecinku ma cena bid
    bid_price_digits = mt5.symbol_info(symbol).digits

    kwotowanie = 10 ** (-bid_price_digits) / 0.1
    kwotowanie = format(kwotowanie, '.5f')
    kwotowanie = float(kwotowanie)

    if (long_position is None) and (df.iloc[-2]['criteria'] == True):
        # oblicz wartość stop loss na podstawie najbliższego minimum
        stop_loss = min(round(df['Low'].iloc[-10:-1], 5))
        # obliczanie stop loss jako odelglosci w pipsach
        stop_loss = int(abs(df.iloc[-1]['Close'] - stop_loss) / kwotowanie)
        # take profit jako 2x stop loss
        take_profit = stop_loss * 2
        # otwórz nową pozycję długą, jeśli nie ma już otwartej pozycji długiej i wystąpił sygnał kupna
        print(f'Otwieranie pozycji dlugiej dla {symbol} o godzinie {time.strftime("%H:%M:%S", time.localtime())}')
        open_long_position_with_sl_tp(symbol, 0.1, stop_loss + 4, take_profit + 4)
    if long_position and symbol not in nie_doji:
        if (df.iloc[-2]['doji'] == True):
            close_all_positions(long_position)




    fig = go.Figure(data=[go.Candlestick(x=df.index,
                    open=df['HA_Open'],
                    high=df['HA_High'],
                    low=df['HA_Low'],
                    close=df['HA_Close'])])
    
    # Dodaj punkty reprezentujące świeczki spełniające kryteria
    fig.add_trace(go.Scatter(x=df[df['criteria']].index, y=df[df['criteria']]['HA_Close'], mode='markers', marker=dict(color='blue', size=10)))

    fig.show()



#########################################################################################################################





def open_short_position(df, symbol):
    nie_doji = ['US10.pro', 'US100.pro', 'US30.pro', 'US500.pro']
    mt5.initialize()
    threshold = 0.03
    body_threshold = 0.15
    # sprawdzenie, czy nie ma już otwartej pozycji krótkiej dla tej samej pary walutowej
    open_positions = mt5.positions_get(symbol=symbol)
    long_position = None
    short_position = None
    for position in open_positions:
        if position.type == mt5.ORDER_TYPE_SELL:
            short_position = position
            break

    # Oblicz świeczki Heikin Ashi (poczatkowe)
    df['HA_Close'] = (df['Open'] + df['High'] + df['Low'] + df['Close']) / 4
    # df['HA_Open'] = (df['Open'].shift(1) + df['Close'].shift(1)) / 2
    df.loc[df.index[0], 'HA_Open'] = df.loc[df.index[0], 'Open'] # pierwsza świeczka HA_Open = Open
    df['HA_High'] = df[['High', 'HA_Open', 'HA_Close']].max(axis=1)
    df['HA_Low'] = df[['Low', 'HA_Open', 'HA_Close']].min(axis=1)

    # oblicz świeczki Heikin Ashi (od polowy)
    for i in range(1, len(df)):
        df.loc[df.index[i], 'HA_Open'] = (df.loc[df.index[i-1], 'HA_Open'] + df.loc[df.index[i-1], 'HA_Close']) / 2

    # popraw świeczki Heikin Ashi
    df['HA_High'] = df[['High', 'HA_Open', 'HA_Close']].max(axis=1)
    df['HA_Low'] = df[['Low', 'HA_Open', 'HA_Close']].min(axis=1)

    # Znajdź świeczki "doji"
    df['doji'] = (abs(df['HA_Close'] - df['HA_Open']) / df['HA_Close']) * 100 < threshold

    # Oblicz EMA dla świeczek Heikin Ashi (długość 30 podczas pierwszego testu)
    df['HA_Close_EMA'] = ta.ema(df['HA_Close'], length=35)

    # Znajdź świeczki spełniające kryteria
    df['criteria'] = False
    prev_doji = False
    for i, row in df.iterrows():
        if prev_doji:
            body_size = abs((row['HA_Close'] - row['HA_Open']) / row['HA_Close']) * 100
            if (row['HA_Close'] < row['HA_Open']) and (row['HA_High'] == row['HA_Open']) and (body_size > body_threshold):
                df.loc[i, 'criteria'] = True
        prev_doji = row['doji']

    # sprawdz ile zer po przecinku ma cena bid
    bid_price_digits = mt5.symbol_info(symbol).digits

    kwotowanie = 10 ** (-bid_price_digits) / 0.1
    kwotowanie = format(kwotowanie, '.5f')
    kwotowanie = float(kwotowanie)
    
    if (short_position is None) and (df.iloc[-2]['criteria'] == True):
        # oblicz wartość stop loss na podstawie najbliższego maksimum
        stop_loss = max(round(df['High'].iloc[-10:-1], 5))
        # otwórz nową pozycję krótką, jeśli nie ma już otwartej pozycji krótkiej i wystąpił sygnał sprzedaży
        stop_loss = int(abs(df.iloc[-1]['Close'] - stop_loss) / kwotowanie)
        # take profit 2x stop loss RR 1:2
        take_profit = stop_loss * 2
        open_short_position_with_sl_tp(symbol, 0.1, stop_loss + 4, take_profit + 4)
        print(f'Otwieranie pozycji krótkiej dla {symbol} o godzinie {time.strftime("%H:%M:%S", time.localtime())}')
    if short_position and symbol not in nie_doji:
        if (df.iloc[-2]['doji'] == True):
            close_all_positions(short_position)





    # fig = go.Figure(data=[go.Candlestick(x=df.index,
    #                 open=df['HA_Open'],
    #                 high=df['HA_High'],
    #                 low=df['HA_Low'],
    #                 close=df['HA_Close'])])
    
    # # Dodaj punkty reprezentujące świeczki spełniające kryteria
    # fig.add_trace(go.Scatter(x=df[df['criteria']].index, y=df[df['criteria']]['HA_Close'], mode='markers', marker=dict(color='blue', size=10)))

    # fig.show()
        

