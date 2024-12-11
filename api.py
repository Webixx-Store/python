import requests
import time
import threading
from binance_client import analyze_signals, get_historical_data
from binance.client import Client
from flask import Flask, jsonify , request
from common import generate_content


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

@app.route('/analyze1', methods=['GET'])
def analyze1():
    try:
        # Lấy các giá trị từ tham số query
        symbol = request.args.get('symbol', default='BTCUSDT')  # Mặc định là 'BTCUSDT' nếu không có tham số
        interval = request.args.get('interval', default='1h')    # Mặc định là '1h'
        limit = int(request.args.get('limit', default=100))      # Mặc định là 100 nếu không có tham số

        # Get historical data
        data = get_historical_data(symbol=symbol, interval=interval, limit=limit)

        # Analyze signals
        analysis = analyze_signals(data, 14)

        message = (
            f"\nTime: {analysis['timestamp']}\n"
            f"Interval: {interval}\n"
            f"Decision: {analysis['decision']} (Strength: {analysis['strength']:.2f}%)\n"
            f"Current Price: {analysis['current_price']}\n\n"
            "Signal Details:\n"
        )
        for signal in analysis['signals_detail']:
            message += f"- {signal}\n"
        
        message += "\nIndicator Values:\n"
        for indicator, value in analysis['indicators'].items():
            message += f"{indicator}: {value:.2f}\n"
        return generate_content("làm ơn hãy phân tích chi tiết cụ thể  từng chỉ báo của dữ liệu này:" + message + " thành 1 bài báo html có font chữ to và phải rõ ràng và không chứa thẻ <html> để tôi inner nó trong thẻ div và trên bài báo phải nêu rõ được xu thế thị trường phân tích giá và xu hướng thị trường 1 cách chi tiết  phần kết luận bạn nên làm to và rõ ràng nổi bật hơn các phần khác	")

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Chạy bot trong một luồng riêng biệt
    threading.Thread(target=call_api, daemon=True).start()

    # Chạy Flask app
    app.run(host='0.0.0.0', port=5000)
