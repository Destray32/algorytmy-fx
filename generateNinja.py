import MetaTrader5 as mt5
import pandas as pd

# połącz z MetaTrader 5
if not mt5.initialize():
    print("initialize() failed")
    mt5.shutdown()

# pobierz dane ceny
rates = mt5.copy_rates_from_pos("EURGBP.pro", mt5.TIMEFRAME_M1, 0, 20000)

# zamknij połączenie z MetaTrader 5
mt5.shutdown()

# przekształć dane w ramkę danych pandas
rates_frame = pd.DataFrame(rates)
rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')

# wybierz kolumny i zmień nazwy kolumn
rates_frame = rates_frame[['time', 'open', 'high', 'low', 'close', 'tick_volume']]
rates_frame.columns = ['date', 'open', 'high', 'low', 'close', 'volume']

# przekształć datę w format yyyyMMdd HHmmss
rates_frame['date'] = rates_frame['date'].dt.strftime('%Y%m%d %H%M%S')


# zapisz dane w pliku txt
rates_frame.to_csv('EURGBP.Last.txt', sep=';', index=False, header=False)
