from time import sleep
import datetime
import MetaTrader5 as mt5

from pobieranie.pobranieDanych import PobranieDanych
# from warunkiWejWyj.warunki import open_long_positions, open_short_position
# from warunkiWejWyj.warunkiKeltnerCh import open_long_position, open_short_position
from warunkiWejWyj.warunki_heiken_doji import open_long_position, open_short_position

def main():
    mt5.initialize()
    symbols = ['US500.pro', 'US100.pro', 'US30.pro', 'EURUSD.pro', 
               'USDJPY.pro', 'USDCAD.pro', "AUDUSD.pro", "USDCHF.pro", "EURJPY.pro"]
    #symbols = ['US500.pro']

    while True:
        # if datetime.datetime.now().hour > 9 and datetime.datetime.now().hour < 22:
        for symbol in symbols:
            dane = PobranieDanych(symbol=symbol, timeframe=mt5.TIMEFRAME_H1, start=0, end=500)
            open_long_position(dane, symbol)
            open_short_position(dane, symbol)
        sleep(30)


if __name__ == '__main__':
    main()