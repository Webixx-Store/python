import logging
from binance.client import Client
from binance.enums import *
from binance_client import analyze_signals, get_historical_data , create_order
import time

# Cấu hình logger
logging.basicConfig(
    filename='trade_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Cấu hình API Key và Secret cho Testnet
API_KEY = '9fe6b1c6e7d43c8aae7f3bbfc60baf40125a7ddd807f82b8d21f2814ba5b1205'
API_SECRET = '06c0cc3bd5b14a74ac90efd6ada9f1642f140b399f333b43e7abc9fd4aff6572'

# Hàm để kết nối với Binance Testnet
def get_binance_client():
    client = Client(API_KEY, API_SECRET, testnet=True)
    client.API_URL = 'https://testnet.binancefuture.com/fapi/v1'
    return client

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

def place_stop_loss(symbol, entry_price, position_side, stop_loss_percent):
    stop_loss_price = entry_price * (1 - stop_loss_percent / 100) if position_side == SIDE_BUY else entry_price * (1 + stop_loss_percent / 100)
    try:
        stop_loss_order = get_binance_client().futures_create_order(
            symbol=symbol,
            side=SIDE_SELL if position_side == SIDE_BUY else SIDE_BUY,
            type=FUTURE_ORDER_TYPE_STOP_MARKET,  # Ensure this constant is defined in the binance.enums
            stopPrice=stop_loss_price,
            quantity=0.0001,  # Thay đổi số lượng theo yêu cầu của bạn
            reduceOnly=True  # Để chỉ chốt lời
        )
        log_trade_event("STOP LOSS", f"Đặt lệnh stop loss cho {symbol} ở mức giá {stop_loss_price:.2f}. Lệnh: {stop_loss_order}")
    except Exception as e:
        log_trade_event("ERROR", f"Lỗi khi đặt lệnh stop loss cho {symbol}: {e}")

def place_take_profit(symbol, entry_price, position_side, take_profit_percent):
    take_profit_price = entry_price * (1 + take_profit_percent / 100) if position_side == SIDE_BUY else entry_price * (1 - take_profit_percent / 100)
    try:
        take_profit_order = get_binance_client().futures_create_order(
            symbol=symbol,
            side=SIDE_SELL if position_side == SIDE_BUY else SIDE_BUY,
            type=FUTURE_ORDER_TYPE_STOP_MARKET,  # Adjust to the correct type if needed
            stopPrice=take_profit_price,
            quantity=0.0001,  # Thay đổi số lượng theo yêu cầu của bạn
            reduceOnly=True  # Để chỉ chốt lời
        )
        log_trade_event("TAKE PROFIT", f"Đặt lệnh take profit cho {symbol} ở mức giá {take_profit_price:.2f}. Lệnh: {take_profit_order}")
    except Exception as e:
        log_trade_event("ERROR", f"Lỗi khi đặt lệnh take profit cho {symbol}: {e}")

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
            place_stop_loss(symbol, entry_price, SIDE_BUY, stop_loss_percent)
            place_take_profit(symbol, entry_price, SIDE_BUY, take_profit_percent)  # Call take profit function
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
            place_stop_loss(symbol, entry_price, SIDE_SELL, stop_loss_percent)
            place_take_profit(symbol, entry_price, SIDE_SELL, take_profit_percent)  # Call take profit function
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
        client = get_binance_client()

        create_order(client ,  0,0.1,SIDE_BUY , FUTURE_ORDER_TYPE_MARKET, True)
        
        trade_based_on_signal(analysis)
    
        time.sleep(10)  # Kiểm tra mỗi phút, thay đổi theo nhu cầu của bạn.

if __name__ == '__main__':
    main()
