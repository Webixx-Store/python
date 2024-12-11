# Sử dụng image Python 3.12.7 mới nhất
FROM python:3.12.7-slim

# Đặt thư mục làm việc trong container
WORKDIR /app

# Sao chép file yêu cầu (requirements.txt) và cài đặt các thư viện
COPY requirements.txt .

# Cài đặt các thư viện trong requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép mã nguồn ứng dụng vào container
COPY . .

# Chạy ứng dụng
CMD ["python", "api.py"]
