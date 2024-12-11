import time
from binance_client import analyze_signals, get_historical_data, get_current_future_price
from binance.client import Client
import logging

# Constants
SYMBOL = "BTCUSDT"
INTERVAL = Client.KLINE_INTERVAL_1MINUTE
LIMIT = 200
TAKE_PROFIT = 300
STOP_LOSS = 300

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

def handle_trade(current_price, side, price_in):
    if side == "BUY":
        if current_price > price_in + TAKE_PROFIT:
            log_trade_event("INFO", f"TAKE PROFIT {SYMBOL} AT: {current_price}")
            return False  # Close position
        elif current_price < price_in - STOP_LOSS:
            log_trade_event("INFO", f"STOP LOSS {SYMBOL} AT: {current_price}")
            return False  # Close position
    elif side == "SELL":
        if current_price < price_in - TAKE_PROFIT:
            log_trade_event("INFO", f"TAKE PROFIT {SYMBOL} AT: {current_price}")
            return False  # Close position
        elif current_price > price_in + STOP_LOSS:
            log_trade_event("INFO", f"STOP LOSS {SYMBOL} AT: {current_price}")
            return False  # Close position
    return True  # Keep position

def main():
    is_position = False
    price_in = 0
    side = ''
    while True:
        data = get_historical_data(symbol=SYMBOL, interval=INTERVAL, limit=LIMIT)
        analysis = analyze_signals(data, 14)
        current_price = get_current_future_price(symbol=SYMBOL)
        if not is_position:
            side = analysis['decision']
            strength = analysis['strength']
            if side in ["BUY", "SELL"] and strength > 70:
                price_in = current_price
                is_position = True
                log_trade_event("INFO", f"{side} {SYMBOL} AT: {current_price}")
            else:
                print(f"Non-action at {SYMBOL}: {current_price}")
        else:  # We are in a position
            is_position = handle_trade(current_price, side, price_in)
        time.sleep(10)  # Adjust based on your strategy
if __name__ == '__main__':
    main()
