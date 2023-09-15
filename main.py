from time import sleep
import datetime
import MetaTrader5 as mt5

from pobieranie.pobranieDanych import PobranieDanych
from warunkiWejWyj.warunki_heiken_doji import open_long_position, open_short_position

def main():
    mt5.initialize()
    symbols = ['US500.pro', 'US100.pro', 'US30.pro', 'EURUSD.pro', 
            'USDJPY.pro', 'USDCAD.pro', "AUDUSD.pro", "USDCHF.pro", "EURJPY.pro"]
    kwotowania = []
    #symbols = ['USDJPY.pro']
    check_news = True

    ObliczKwotowanie(symbols, kwotowania)

    while True:
        # if datetime.datetime.now().hour > 9 and datetime.datetime.now().hour < 22:
        for symbol in symbols:
            dane = PobranieDanych(symbol=symbol, timeframe=mt5.TIMEFRAME_H1, start=0, end=500)
            open_long_position(dane, symbol, kwotowania[symbols.index(symbol)], check_news)
            open_short_position(dane, symbol, kwotowania[symbols.index(symbol)], check_news)
        sleep(100)


def ObliczKwotowanie(symbols, kwotowania):
    """
    Calculates the quoting precision for each symbol in the given list of symbols and appends it to the given list of quoting precisions.

    Args:
    symbols (list): A list of symbols for which the quoting precision needs to be calculated.
    kwotowania (list): A list to which the calculated quoting precisions will be appended.

    Returns:
    None
    """
    for symbol in symbols:
        bid_price_digits = mt5.symbol_info(symbol).digits

        kwotowanie = 10 ** (-bid_price_digits) / 0.1
        kwotowanie = format(kwotowanie, '.5f')
        kwotowanie = float(kwotowanie)

        kwotowania.append(kwotowanie)



if __name__ == '__main__':
    main()