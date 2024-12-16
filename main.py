from binance_client import  get_historical_data , get_current_future_price


def main():
    data = get_current_future_price(symbol='BTCUSDT')
    print(data)
      
if __name__ == '__main__':
    main()