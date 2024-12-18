from binance_client import  get_historical_data , get_current_future_price


def main():
    symbol = 'ETHUSDT'
    data = get_current_future_price(symbol=symbol)
    message = (
            f"\nSymbol: {symbol}\n"
            f"\nCurrentPrice: {data}\n"
            "Signal Details:\n"
        )
    print(message)
      
if __name__ == '__main__':
    main()