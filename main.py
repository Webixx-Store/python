import requests
import json
from binance_client import analyze_signals , get_historical_data
from binance.client import Client
from binance.enums import *


def generate_content( prompt):
    api_key = 'AIzaSyCNHcjHExhYkmoIekWcwCKveNqd5i60yXs' 
    url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent'
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        'contents': [
            {
                'parts': [
                    {
                        'text': prompt
                    }
                ]
            }
        ]
    }
    response = requests.post(url, headers=headers, params={'key': api_key}, json=data)
    if response.status_code == 200:
        return  response.json()['candidates'][0]['content']['parts'][0]['text']  # Return the JSON response if the request was successful
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")

# Example usage
 # Replace with your actual API key
prompt = 'ĐÂY LÀ DỮ LIỆU THỰC TẾ Ở THỜI ĐIỂM HIỆN TẠI BẠN HÃY PHÂN TÍCH CỤ THỂ 1 CÁCH CHI TIẾT ĐỂ NGƯỜI DÙNG HIỂU VÀ ĐƯA RA KHẢ NĂNG CỦA DỮ LIỆU NÀY'
try:
    symbol = 'BTCUSDT'
    interval = Client.KLINE_INTERVAL_1MINUTE
    limit = 200
    df = get_historical_data(symbol, interval, limit)
    analysis = analyze_signals(df)
    result = generate_content( prompt + str(analysis) )
    print(result)  # Print the result in a readable format

except Exception as e:
    print(e)


        