import requests
import time
import threading
from binance_client import analyze_signals, get_historical_data
from binance.client import Client
from flask import Flask, jsonify

# Constants
SYMBOL = "BTCUSDT"
INTERVAL = Client.KLINE_INTERVAL_1MINUTE
LIMIT = 200
TAKE_PROFIT = 300
STOP_LOSS = 300

app = Flask(__name__)

# Hàm gửi yêu cầu GET đến API của bạn
def call_api():
    url = "https://python-fk3x.onrender.com"  # Thay đổi với URL thực tế của bạn
    while True:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print("Yêu cầu thành công!")
                print("Nội dung phản hồi:")
                print(response.text)
            else:
                print(f"Yêu cầu thất bại. Mã trạng thái: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Đã có lỗi xảy ra: {e}")
        
        time.sleep(30)  # Đợi 30 giây trước khi gọi lại

@app.route('/analyze', methods=['GET'])
def analyze():
    try:
        # Get historical data
        data = get_historical_data(symbol=SYMBOL, interval=INTERVAL, limit=LIMIT)

        # Analyze signals
        analysis = analyze_signals(data, 14)
        return analysis

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Chạy bot trong một luồng riêng biệt
    threading.Thread(target=call_api, daemon=True).start()

    # Chạy Flask app
    app.run(host='0.0.0.0', port=5000)
