from time import sleep
import MetaTrader5 as mt5

from pobieranie.pobranieDanych import PobranieDanych
# from warunkiWejWyj.warunki import open_long_positions, open_short_position
# from warunkiWejWyj.warunkiKeltnerCh import open_long_position, open_short_position
from warunkiWejWyj.warunki_heiken_doji import open_long_position, open_short_position

# Na Ninjatraderze jest to strategia o nazwie BolllingerBands coś tam i trójka na końcu

def main():
    mt5.initialize()
    symbols = ['US500.pro', 'US30.pro', 'US100.pro', 'EURUSD.pro', 
               'GBPUSD.pro', 'USDJPY.pro', 'USDCHF.pro', 'AUDUSD.pro']

    while True:
        for symbol in symbols:
            dane = PobranieDanych(symbol=symbol, timeframe=mt5.TIMEFRAME_H1, start=0, end=400)
            open_long_position(dane, symbol)
            open_short_position(dane, symbol)
        sleep(10)


if __name__ == '__main__':
    main()