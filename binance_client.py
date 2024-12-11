from binance.client import Client
import configparser
from typing import Tuple
import pandas_ta as ta
import pandas as pd
from binance.enums import *
test_net = True
def load_config(file_path: str) -> Tuple[str, str]:
    try:
        config = configparser.ConfigParser()
        config.read(file_path)

        api_key = config['BINANCE']['api_key']
        api_secret = config['BINANCE']['api_secret']
        api_key_testnet = config['BINANCE']['api_key_testnet']
        api_secret_testnet = config['BINANCE']['api_secret_testnet']
        return api_key, api_secret , api_key_testnet , api_secret_testnet
        
    except Exception as e:
        raise Exception(f"Error loading config: {str(e)}")

def get_binance_client() -> Client:
    try:
        api_key, api_secret ,api_key_testnet , api_secret_testnet = load_config("config.properties")
        client = Client(api_key_testnet if test_net else api_key
                    , api_secret_testnet if test_net else api_secret 
                    , testnet= test_net)
        if test_net:
           client.API_URL = 'https://testnet.binancefuture.com/fapi/v1'
        return client
    except Exception as e:
        raise Exception(f"Error creating Binance client: {str(e)}")
    


def get_closing_prices(symbol: str, interval: str, limit: int) -> list:
    try:
        client = get_binance_client()
        klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
        return [float(candle[4]) for candle in klines]
    except Exception as e:
        raise Exception(f"Error fetching prices: {str(e)}")
    
def calculate_rsi(close_prices, period=14):
    try:
        import pandas as pd
        close_prices = pd.Series(close_prices)
        rsi = ta.rsi(close_prices, length=period)
        return float(rsi.dropna().iloc[-1])  # Bỏ qua các giá trị None và lấy giá trị cuối
    except Exception as e:
        raise Exception(f"Error calculating RSI: {str(e)}")

def get_historical_data(symbol, interval, limit=200):
    try:
        client = get_binance_client()
        klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
        
        # Chuyển đổi dữ liệu thành DataFrame
        df = pd.DataFrame(klines, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_asset_volume', 'number_of_trades',
            'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
        ])
        
        # Chuyển đổi kiểu dữ liệu
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df['close_time'] = pd.to_datetime(df['close_time'], unit='ms')
        
        # Chuyển các cột giá và volume thành float
        numeric_columns = ['open', 'high', 'low', 'close', 'volume',
                         'quote_asset_volume', 'taker_buy_base_asset_volume',
                         'taker_buy_quote_asset_volume']
        
        df[numeric_columns] = df[numeric_columns].astype(float)
        
        return df
    
    except Exception as e:
        raise Exception(f"Error getting historical data: {str(e)}")

def analyze_signals(df, period=14):
    try:
        # Tính toán các chỉ báo
        indicators = {}
        
        # RSI
        indicators['rsi'] = ta.rsi(df['close'], length=period)
        
        # MACD
        macd = ta.macd(df['close'])
        indicators['macd_line'] = macd['MACD_12_26_9']
        indicators['macd_signal'] = macd['MACDs_12_26_9']
        
        # Bollinger Bands
        bbands = ta.bbands(df['close'], length=20)
        indicators['bb_upper'] = bbands['BBU_20_2.0']
        indicators['bb_middle'] = bbands['BBM_20_2.0']
        indicators['bb_lower'] = bbands['BBL_20_2.0']
        
        # Stochastic
        stoch = ta.stoch(df['high'], df['low'], df['close'])
        indicators['stoch_k'] = stoch['STOCHk_14_3_3']
        indicators['stoch_d'] = stoch['STOCHd_14_3_3']

        # Moving Averages
        indicators['sma_20'] = ta.sma(df['close'], length=20)
        indicators['sma_50'] = ta.sma(df['close'], length=50)

        # Lấy giá trị mới nhất
        latest = {k: float(v.iloc[-1]) for k, v in indicators.items()}
        current_price = float(df['close'].iloc[-1])

        # Phân tích tín hiệu
        buy_signals = 0
        sell_signals = 0
        signals_detail = []

        # 1. RSI Analysis
        if latest['rsi'] < 30:
            buy_signals += 2
            signals_detail.append("RSI oversold (< 30) - Strong Buy Signal")
        elif latest['rsi'] < 40:
            buy_signals += 1
            signals_detail.append("RSI near oversold (< 40) - Weak Buy Signal")
        elif latest['rsi'] > 70:
            sell_signals += 2
            signals_detail.append("RSI overbought (> 70) - Strong Sell Signal")
        elif latest['rsi'] > 60:
            sell_signals += 1
            signals_detail.append("RSI near overbought (> 60) - Weak Sell Signal")

        # 2. MACD Analysis
        if latest['macd_line'] > latest['macd_signal']:
            buy_signals += 1
            signals_detail.append("MACD above Signal Line - Buy Signal")
        else:
            sell_signals += 1
            signals_detail.append("MACD below Signal Line - Sell Signal")

        # 3. Bollinger Bands Analysis
        if current_price < latest['bb_lower']:
            buy_signals += 2
            signals_detail.append("Price below Lower BB - Strong Buy Signal")
        elif current_price > latest['bb_upper']:
            sell_signals += 2
            signals_detail.append("Price above Upper BB - Strong Sell Signal")

        # 4. Stochastic Analysis
        if latest['stoch_k'] < 20 and latest['stoch_d'] < 20:
            buy_signals += 1
            signals_detail.append("Stochastic Oversold - Buy Signal")
        elif latest['stoch_k'] > 80 and latest['stoch_d'] > 80:
            sell_signals += 1
            signals_detail.append("Stochastic Overbought - Sell Signal")

        # 5. Moving Average Analysis
        if latest['sma_20'] > latest['sma_50']:
            buy_signals += 1
            signals_detail.append("SMA20 above SMA50 - Bullish Trend")
        else:
            sell_signals += 1
            signals_detail.append("SMA20 below SMA50 - Bearish Trend")

        # Tổng hợp kết quả
        total_signals = buy_signals + sell_signals
        buy_strength = (buy_signals / total_signals) * 100 if total_signals > 0 else 50
        sell_strength = (sell_signals / total_signals) * 100 if total_signals > 0 else 50

        # Đưa ra quyết định
        if buy_signals > sell_signals:
            decision = "BUY"
            strength = buy_strength
        elif sell_signals > buy_signals:
            decision = "SELL"
            strength = sell_strength
        else:
            decision = "NEUTRAL"
            strength = 50

        result = {
            'decision': decision,
            'strength': strength,
            'buy_signals': buy_signals,
            'sell_signals': sell_signals,
            'current_price': current_price,
            'indicators': latest,
            'signals_detail': signals_detail,
            'timestamp': df['timestamp'].iloc[-1]
        }

        return result

    except Exception as e:
        raise Exception(f"Error analyzing signals: {str(e)}")
    
def get_tick_size(symbol):
    # Lấy thông tin về cặp giao dịch từ Binance
    exchange_info = get_binance_client().futures_exchange_info()
    for symbol_info in exchange_info['symbols']:
        if symbol_info['symbol'] == symbol:
            for filter in symbol_info['filters']:
                if filter['filterType'] == 'PRICE_FILTER':
                    return float(filter['tickSize'])  # Trả về tick size
    return 0.01  # Nếu không tìm thấy, mặc định trả về tick size là 0.01

def round_to_tick_size(price, tick_size):
    # Làm tròn giá về bội số của tick size
    return round(price / tick_size) * tick_size
    
def create_order(symbol, price, quantity, side, order_type):
    try:
        parameters = {
         "symbol": symbol,
         "side": side,
         "quantity": format(quantity, ".3f"),
         "type": order_type,
        }
        tick_size = get_tick_size(symbol)
        rounded_price = round_to_tick_size(price, tick_size)

        if order_type in {FUTURE_ORDER_TYPE_LIMIT, FUTURE_ORDER_TYPE_STOP, FUTURE_ORDER_TYPE_TAKE_PROFIT}:
            parameters["price"] = format(price, ".2f")
            parameters["timeInForce"] = "GTC"
        if order_type in {FUTURE_ORDER_TYPE_STOP_MARKET, FUTURE_ORDER_TYPE_TAKE_PROFIT_MARKET,
                        FUTURE_ORDER_TYPE_STOP, FUTURE_ORDER_TYPE_TAKE_PROFIT}:
            parameters["stopPrice"] = format(price, ".2f")
        # Gọi client.create_order với các tham số đúng cách
        return get_binance_client().futures_create_order(
            symbol=symbol,
            side=side,
            quantity=format(quantity, ".3f"),
            type=order_type,
            price=format(rounded_price, ".2f") if 'price' in parameters else None,
            stopprice=format(rounded_price, ".2f") if 'stopPrice' in parameters else None
        )
    
    except Exception as e:
        raise Exception(f"Order failed: {str(e)}")
    
def get_current_future_price(symbol):
    try:
        # Lấy giá hiện tại của hợp đồng tương lai
        futures_price = get_binance_client().futures_symbol_ticker(symbol=symbol)
        return float(futures_price['price'])
    except Exception as e:
        print(f"Error getting current price: {e}")
        return None
    

def getAmtPosition(symbol) -> float:
    try:
        position = get_binance_client().futures_position_information()
        first_data = next((item for item in position if item['symbol'] == symbol), None)
        return float(first_data['positionAmt'])
    except Exception as e:
        return 0
