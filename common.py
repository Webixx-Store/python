from datetime import datetime
import requests
import json
def convert_timestamp_to_yyyymmddhhmmss(timestamp):
    # Chuyển đổi timestamp từ milliseconds sang seconds
    timestamp_seconds = timestamp / 1000.0
    
    # Chuyển đổi sang đối tượng datetime
    dt_object = datetime.fromtimestamp(timestamp_seconds)
    
    # Định dạng lại thành chuỗi theo định dạng 'YYYYMMDDHHMMSS'
    formatted_time = dt_object.strftime('%Y%m%d%H%M%S')
    
    return formatted_time

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
