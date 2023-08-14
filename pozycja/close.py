import MetaTrader5 as mt5

def close_all_positions(symbol):
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

    # pobranie otwartych pozycji dla podanego symbolu
    open_positions = mt5.positions_get(symbol=symbol)
    for position in open_positions:
        # przygotowanie zlecenia zamknięcia pozycji
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "position": position.ticket,
            "symbol": symbol,
            "volume": position.volume,
            "type": mt5.ORDER_TYPE_SELL if position.type == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_BUY,
            "price": mt5.symbol_info_tick(symbol).bid if position.type == mt5.ORDER_TYPE_BUY else mt5.symbol_info_tick(symbol).ask,
            "magic": 234000,
            "comment": "python script close",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_FOK,
        }

        # wysłanie zlecenia zamknięcia pozycji
        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print(f"order_send failed, retcode={result.retcode}")
        else:
            print(f"order_send succeeded, order_id={result.order}")

