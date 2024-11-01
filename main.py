
from binance_client import  create_order, get_current_future_price 
from binance.enums  import *
def main():
    try:
       # create order market
       create_order(  'BTCUSDT' ,0,0.1,SIDE_BUY , FUTURE_ORDER_TYPE_MARKET)
       entry_price = get_current_future_price("BTCUSDT")
       # create profit
       create_order( 'BTCUSDT' , entry_price + 1000 , 0.1 , SIDE_SELL  , FUTURE_ORDER_TYPE_TAKE_PROFIT_MARKET )
        # create stoplost
       create_order( 'BTCUSDT' , entry_price - 1000 , 0.1 , SIDE_SELL  , FUTURE_ORDER_TYPE_STOP_MARKET )

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()