import time
from binance_client import analyze_signals, get_historical_data, get_current_future_price , create_order , get_binance_client , getAmtPosition
from binance.client import Client
import logging
from binance.enums import *
# Constants
SYMBOL = "BTCUSDT"
INTERVAL = Client.KLINE_INTERVAL_1MINUTE
LIMIT = 200
# Configure logger
logging.basicConfig(
    filename='trade_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Log trade events
def log_trade_event(event_type, message):
    logging.info(f"{event_type} - {message}")
    print(f"{event_type} - {message}")

def trace(symbol , side , handlePrice , quantity):
    order = create_order(
                symbol=symbol,
                price=0,
                quantity=quantity,
                side=side,
                order_type=FUTURE_ORDER_TYPE_MARKET
            )
    getOrder = get_binance_client().futures_get_order(id =  order['orderId'])
    avgPrice = float(getOrder['avgPrice'])
    takeProfit = 0
    stoploss   = 0
    if side == SIDE_BUY:
        takeProfit = avgPrice + handlePrice
        stoploss   = avgPrice - handlePrice
    elif side == SIDE_SELL:
        takeProfit = avgPrice - handlePrice
        stoploss   = avgPrice + handlePrice
    order1  = create_order(
                 symbol=symbol,
                 price=takeProfit,
                 quantity=0.01,
                 side= SIDE_SELL if side == SIDE_BUY else SIDE_BUY,
                 order_type=FUTURE_ORDER_TYPE_TAKE_PROFIT
             )
    order2  = create_order(
                 symbol=symbol,
                 price=stoploss,
                 quantity=0.01,
                 side= SIDE_SELL if side == SIDE_BUY else SIDE_BUY,
                 order_type=FUTURE_ORDER_TYPE_STOP
             )
def main():
    while True:
        data = get_historical_data(symbol=SYMBOL, interval=INTERVAL, limit=LIMIT)
        analysis = analyze_signals(data, 14)
        current_price = get_current_future_price(symbol=SYMBOL)
        amtPosition = getAmtPosition(symbol=SYMBOL)
        if amtPosition == 0:
            side = analysis['decision']
            strength = analysis['strength']
            if side in ["BUY", "SELL"] and strength > 70:
                get_binance_client().futures_cancel_all_open_orders(symbol = SYMBOL)
                trace(symbol=SYMBOL , side= side  , handlePrice=1000 , quantity=0.1)
                log_trade_event("INFO", f"{side} {SYMBOL} AT: {current_price}")
            else:
                print(f"Non-action at {SYMBOL}: {current_price}")
        time.sleep(20)
if __name__ == '__main__':
  main()

