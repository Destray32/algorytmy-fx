import MetaTrader5 as mt5
import time
import pandas_ta as ta
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from pozycja.long import open_long_position_with_sl_tp
from pozycja.short import open_short_position_with_sl_tp
from pozycja.close import close_all_positions

from kalendarz.kalendarz_eko import Kalendarz

# Dodaj zmienną, która liczy, ile razy PSAR się zmienił
psar_change = 0

# TODO:

def open_position(df, symbol, kwotowanie, newsChecking, position_type):
    # position_type może być 'long' lub 'short'
    
    nie_doji = ['US10.pro', 'US100.pro', 'US30.pro', 'US500.pro']
    flaga = False
    highImpactNews = False
    mt5.initialize()

    try:
        # obliczanie spreadu
        spread = mt5.symbol_info(symbol).spread * mt5.symbol_info(symbol).point
    except:
        spread = 0
        print(f"Nie udało się obliczyć spreadu dla {symbol}")

    # Pobranie kalendarza ekonomicznego i czasu w którym wstrzymać się od handlu
    if (symbol not in nie_doji):
        kalendarz = Kalendarz([symbol[:3], symbol[3:6]])
        kalendarz.PobierzDaty()
        kalendarz.ZnajdzGodzineWstecz()
        kalendarz.ZnajdzGodzinePo()

        # Sprawdzenie czy wstrzymać się od handlu
        highImpactNews = kalendarz.CzyHighImpact(ile_godzin_wstecz=4)
    else:
        kalendarz = Kalendarz("USD")
        kalendarz.PobierzDaty()
        kalendarz.ZnajdzGodzineWstecz()
        kalendarz.ZnajdzGodzinePo()

        # Sprawdzenie czy wstrzymać się od handlu
        highImpactNews = kalendarz.CzyHighImpact(ile_godzin_wstecz=4)


    
    try:
        # sprawdzenie, czy nie ma już otwartej pozycji dla tej samej pary walutowej
        open_positions = mt5.positions_get(symbol=symbol)
        position = None
        if open_positions is not None:
            for p in open_positions:
                type = p.type

                if type == mt5.ORDER_TYPE_BUY and position_type == 'long':
                    position = p
                    flaga = True
                    break
                elif type == mt5.ORDER_TYPE_SELL and position_type == 'short':
                    position = p
                    flaga = True
                    break
        else:
            flaga = False


        df['PSAR_DOWN'] = df.ta.psar(high=df['High'], low=df['Low'], close=df['Close'], af0=0.01, af=0.01, max_af=0.2)['PSARl_0.01_0.2']
        df['PSAR_UP'] = df.ta.psar(high=df['High'], low=df['Low'], close=df['Close'], af0=0.01, af=0.01, max_af=0.2)['PSARs_0.01_0.2']

        df['ATR'] = df.ta.atr(high=df['High'], low=df['Low'], close=df['Close'], length=1)


        # Dodaj kolumny span_a i span_b z funkcji ichimoku
        ichimoku = ta.ichimoku(high=df['High'], low=df['Low'], close=df['Close'])
        df = pd.concat([df, ichimoku[0]], axis=1)

        # Znajdź świeczki spełniające kryteria
        df['criteria'] = False
        criteria_met = False
        for i, row in df.iterrows():
            # warunek sprawdza cene w stosunku do chmury ichimoku i PSAR
            if position_type == 'long':
                # dla pozycji długiej, cena musi być powyżej chmury i PSAR_DOWN
                if df.loc[i, 'Close'] > df.loc[i, 'ISA_9'] and df.loc[i, 'Close'] > df.loc[i, 'ISB_26'] and not np.isnan(df.loc[i, 'PSAR_DOWN']) and not criteria_met:
                    df.loc[i, 'criteria'] = True
                    criteria_met = True
                else:
                    df.loc[i, 'criteria'] = False
                    if np.isnan(df.loc[i, 'PSAR_DOWN']):
                        criteria_met = False
            elif position_type == 'short':
                # dla pozycji krótkiej, cena musi być poniżej chmury i PSAR_UP
                if df.loc[i, 'Close'] < df.loc[i, 'ISA_9'] and df.loc[i, 'Close'] < df.loc[i, 'ISB_26'] and not np.isnan(df.loc[i, 'PSAR_UP']) and not criteria_met:
                    df.loc[i, 'criteria'] = True
                    criteria_met = True
                else:
                    df.loc[i, 'criteria'] = False
                    if np.isnan(df.loc[i, 'PSAR_UP']):
                        criteria_met = False

        # Sprawdź, czy PSAR jest w fazie poczatkowej
        czy_poczatek_psar = False

        if position_type == 'long':
            # dla pozycji długiej, sprawdź czy PSAR_DOWN jest na początku
            if np.isnan(df.iloc[-4]['PSAR_DOWN']):
                czy_poczatek_psar = True
            else:
                czy_poczatek_psar = False
        elif position_type == 'short':
            # dla pozycji krótkiej, sprawdź czy PSAR_UP jest na początku
            if np.isnan(df.iloc[-4]['PSAR_UP']):
                czy_poczatek_psar = True
            else:
                czy_poczatek_psar = False



        if (highImpactNews is True) and (newsChecking):
            print(f'Wstrzymanie się od handlu dla {symbol} o godzinie {time.strftime("%H:%M:%S", time.localtime())}')
            close_all_positions(symbol)
            return


        if ((flaga is False) and (df.iloc[-2]['criteria'] == True) and (psar_change >= 2) and (czy_poczatek_psar is True)):
            # otwórz nową pozycję, jeśli nie ma już otwartej pozycji, wystąpił sygnał, ostatnia pozycja była inna i PSAR zmienił się dwa razy
            print(f'Otwieranie pozycji {position_type} dla {symbol} o godzinie {time.strftime("%H:%M:%S", time.localtime())}')
            if position_type == 'long':
                # otwórz pozycję długą
                open_long_position_with_sl_tp(symbol, 0.1, (df.iloc[-2]['ATR'] * 0.65) + spread, (df.iloc[-2]['ATR'] * 0.65) - spread, False, 0.1, True)
            elif position_type == 'short':
                # otwórz pozycję krótką
                open_short_position_with_sl_tp(symbol, 0.1, (df.iloc[-2]['ATR'] * 0.65) + spread, (df.iloc[-2]['ATR'] * 0.65) - spread, False, 0.1, True)
            # Zresetuj zmienną liczącą zmianę PSAR
            psar_change = 0

        if (flaga is True) and ((np.isnan(df.iloc[-2]['PSAR_DOWN']) and position_type == 'long') or (np.isnan(df.iloc[-2]['PSAR_UP']) and position_type == 'short')):
            # zamknij pozycję, jeśli wystąpił sygnał przeciwny
            print(f'Zamykanie pozycji {position_type} dla {symbol} o godzinie {time.strftime("%H:%M:%S", time.localtime())}')
            close_all_positions(symbol)

        # Sprawdź, czy PSAR się zmienił
        # ta metoda jest tylko w tej funkcji bo gdybym dał ją w obu funkcjach to by się zwiększała dwukrotnie
        if (not np.isnan(df.iloc[-2]['PSAR_DOWN']) and not np.isnan(df.iloc[-3]['PSAR_UP'])) or (not np.isnan(df.iloc[-2]['PSAR_UP']) and not np.isnan(df.iloc[-3]['PSAR_DOWN'])):
            # Jeśli tak, zwiększ zmienną liczącą zmianę PSAR o 1
            psar_change += 1
            print(f'PSAR zmienił się {psar_change} razy dla {symbol} o godzinie {time.strftime("%H:%M:%S", time.localtime())}')


    except Exception as e:
        print(f"An error occurred in opening function: {e}")

    #print("Flaga: ", flaga)
        
    # fig = go.Figure(data=[go.Candlestick(x=df['time'],
    #                 open=df['Open'],
    #                 high=df['High'],
    #                 low=df['Low'],
    #                 close=df['Close'])])
    # fig.add_trace(go.Scatter(x=df['time'], y=df['PSAR_UP'], mode='lines', name='PSAR_UP'))
    # fig.add_trace(go.Scatter(x=df['time'], y=df['PSAR_DOWN'], mode='lines', name='PSAR_DOWN'))
    # fig.add_trace(go.Scatter(x=df['time'], y=df['ISA_9'], mode='lines', name='ISA_9'))
    # fig.add_trace(go.Scatter(x=df['time'], y=df['ISB_26'], mode='lines', name='ISB_26'))
    # fig.add_trace(go.Scatter(x=df['time'], y=df['criteria'], mode='markers', name='criteria'))
    # fig.show()


        

