import logging
from binance.client import Client
from binance.enums import *
from binance_client import analyze_signals, get_historical_data , create_order , get_binance_client
import time

# Cấu hình logger
logging.basicConfig(
    filename='trade_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
# Hàm ghi log
def log_trade_event(event_type, message):
    logging.info(f"{event_type} - {message}")
    print(f"{event_type} - {message}")

def has_open_position(symbol='BTCUSDT'):
    try:
        positions = get_binance_client().futures_account()['positions']
        for position in positions:
            if position['symbol'] == symbol and float(position['positionAmt']) != 0:
                log_trade_event("INFO", f"Lệnh đang mở cho {symbol}. Không đặt lệnh mới.")
                return True
        return False
    except Exception as e:
        log_trade_event("ERROR", f"Lỗi khi kiểm tra lệnh mở: {e}")
        return True  # Trả về True để không vào lệnh nếu lỗi xảy ra


def trade_based_on_signal(analysis, symbol='BTCUSDT', quantity=0.1, stop_loss_percent=2.0, take_profit_percent=5.0):
    if has_open_position(symbol):
        return
    
    decision = analysis['decision']
    strength = analysis['strength']
    
    if decision == "BUY" and strength >= 75:
        try:
            order = get_binance_client().futures_create_order(
                symbol=symbol,
                side=SIDE_BUY,
                type=ORDER_TYPE_MARKET,
                quantity=quantity
            )
            entry_price = float(order['fills'][0]['price'])
            log_trade_event("OPEN", f"Mua (Long) {quantity} {symbol} Futures. Lệnh: {order}")
            return order
        except Exception as e:
            log_trade_event("ERROR", f"Lỗi khi đặt lệnh BUY cho {symbol}: {e}")
    elif decision == "SELL" and strength >= 75:
        try:
            order = get_binance_client().futures_create_order(
                symbol=symbol,
                side=SIDE_SELL,
                type=ORDER_TYPE_MARKET,
                quantity=quantity
            )
            entry_price = float(order['fills'][0]['price'])
            log_trade_event("OPEN", f"Bán (Short) {quantity} {symbol} Futures. Lệnh: {order}")
            return order
        except Exception as e:
            log_trade_event("ERROR", f"Lỗi khi đặt lệnh SELL cho {symbol}: {e}")
    else:
        log_trade_event("INFO", "Chưa có tín hiệu đủ mạnh để giao dịch.")
        return None

async  def  main():
    symbol = 'BTCUSDT'
    interval = Client.KLINE_INTERVAL_1MINUTE
    limit = 200
    while True:
        df = get_historical_data(symbol, interval, limit)
        analysis = analyze_signals(df)
        trade_based_on_signal(analysis)
        time.sleep(10)  # Kiểm tra mỗi phút, thay đổi theo nhu cầu của bạn.
if __name__ == '__main__':
    main()
