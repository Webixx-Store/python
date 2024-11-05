import time
from binance_client import analyze_signals , get_historical_data , get_current_future_price
from binance.client import Client
from binance.enums import *
import logging
#declare available
symbol = "BTCUSDT"
interval = Client.KLINE_INTERVAL_1MINUTE
limit = 200
priceIn = 0
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


def  main():
    count = 0
    countFail = 0
    countSuscess = 0
    isPosition = False
    priceIn = 0
    while True:
        data = get_historical_data(symbol=symbol, interval=interval ,  limit=limit)
        ana = analyze_signals(data , 14)
        strength = 0
        side = ''
        currentPrice  = get_current_future_price(symbol=symbol)
        if isPosition == False:
            side = ana['decision']
            strength = ana['strength']
            if side == "BUY" and strength > 70:
               count += 1
               priceIn =currentPrice
               isPosition = True
               log_trade_event("INFO"  ,side + " " + symbol + " AT: " + str(currentPrice))
            elif side == "SELL" and strength > 70:
               count += 1
               priceIn = currentPrice
               isPosition = True
               log_trade_event("INFO"  ,side + " " + symbol + " AT: " + str(currentPrice))
            else:
                print("Non - action at " + symbol + ": " + str(currentPrice))
        ## takeProfit    
        if isPosition == True:
            takeProfit = 300
            stoploss   = 300
            if side == "BUY":
                if(priceIn > currentPrice + takeProfit):
                    countSuscess += 1
                    log_trade_event("INFO"  ,"TAKE PROFIT" + " " + symbol + " AT: " + str(currentPrice))
                    isPosition = False
                elif priceIn < currentPrice - stoploss:
                    countFail += 1
                    log_trade_event("INFO"  ,"STOP LOST" + " " + symbol + " AT: " + str(currentPrice)) 
                    isPosition = False 

            elif side == "SELL":
                if(priceIn < currentPrice - takeProfit):
                    countSuscess += 1
                    log_trade_event("INFO"  ,"TAKE PROFIT" + " " + symbol + " AT: " + str(currentPrice))
                    isPosition = False
                elif priceIn > currentPrice + stoploss:
                    countFail += 1
                    log_trade_event("INFO"  ,"STOP LOST" + " " + symbol + " AT: " + str(currentPrice))
                    isPosition = False
            else:
                print( "PROPORTION: " + priceIn / currentPrice * 100 )
        
        time.sleep(10)
            
       


     



    #while True:
    #   time.sleep(10)  # Kiểm tra mỗi phút, thay đổi theo nhu cầu của bạn.
if __name__ == '__main__':
    main()