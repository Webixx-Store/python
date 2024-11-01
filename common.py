from datetime import datetime

def convert_timestamp_to_yyyymmddhhmmss(timestamp):
    # Chuyển đổi timestamp từ milliseconds sang seconds
    timestamp_seconds = timestamp / 1000.0
    
    # Chuyển đổi sang đối tượng datetime
    dt_object = datetime.fromtimestamp(timestamp_seconds)
    
    # Định dạng lại thành chuỗi theo định dạng 'YYYYMMDDHHMMSS'
    formatted_time = dt_object.strftime('%Y%m%d%H%M%S')
    
    return formatted_time
