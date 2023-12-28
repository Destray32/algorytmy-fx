import MetaTrader5 as mt5

def open_short_position_with_sl_tp(symbol, volume, sl_pips, tp_pips, percentMode=False, percent=0.1, pominKwotowanie=False):
    # połączenie z MetaTrader 5
    if not mt5.initialize():
        print("initialize() failed")
        mt5.shutdown()
        return

    # pobranie informacji o symbolu
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        print(f"{symbol} not found")
        mt5.shutdown()
        return

    # sprawdz ile zer po przecinku ma cena bid
    bid_price_digits = mt5.symbol_info(symbol).digits

    kwotowanie = 10 ** (-bid_price_digits) / 0.1
    kwotowanie = format(kwotowanie, '.5f')
    kwotowanie = float(kwotowanie)

    if not pominKwotowanie:
        # obliczenie wartości stop loss i take profit w punktach
        point = kwotowanie
        sl_points = round(sl_pips * point, 5)
        tp_points = round(tp_pips * point, 5)
    else:
        sl_points = sl_pips
        tp_points = tp_pips

    if percentMode:
        # pobranie ceny bid
        bid = mt5.symbol_info_tick(symbol).bid

        # obliczenie ceny stop loss i take profit
        sl_price = bid * (1 + percent)
        tp_price = bid * (1 - percent - 0.05)
    else:
        # pobranie ceny bid
        bid = mt5.symbol_info_tick(symbol).bid

        # obliczenie ceny stop loss i take profit
        sl_price = bid + sl_points
        tp_price = bid - tp_points


    # przygotowanie zlecenia sprzedaży
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": mt5.ORDER_TYPE_SELL,
        "price": bid,
        "sl": sl_price,
        "tp": tp_price,
        "magic": 234000,
        "comment": "python script open",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_FOK,
    }

    # wysłanie zlecenia sprzedaży
    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"order_send failed, retcode={result.retcode}")
    else:
        print(f"order_send succeeded, order_id={result.order}")
