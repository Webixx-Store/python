from binance_client import analyze_signals, get_historical_data
from binance.client import Client
from flask import Flask, request, jsonify


# Constants
SYMBOL = "BTCUSDT"
INTERVAL = Client.KLINE_INTERVAL_1MINUTE
LIMIT = 200
TAKE_PROFIT = 300
STOP_LOSS = 300

app = Flask(__name__)

@app.route('/analyze', methods=['GET'])
def analyze():
    # Get query parameters
    symbol = 'BTCUSDT'
    # interval = request.args.get('interval', '1D')
    # limit = int(request.args.get('limit', 100))
    
    try:
        # Get historical data
        data = get_historical_data(symbol=SYMBOL, interval=INTERVAL, limit=LIMIT)

        # Analyze signals
        analysis = analyze_signals(data, 14)
        return analysis

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
