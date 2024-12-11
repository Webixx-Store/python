# Sử dụng image Python 3.12.7 mới nhất
FROM python:3.12.7-slim

# Đặt thư mục làm việc trong container
WORKDIR /app

# Cập nhật pip lên phiên bản mới nhất
RUN pip install --upgrade pip

# Cài đặt setuptools trước để tránh lỗi với các thư viện cần biên dịch
RUN pip install --no-cache-dir setuptools

# Cài đặt build-essential và python3-dev cho các thư viện cần biên dịch
RUN apt-get update && apt-get install -y build-essential python3-dev

# Sao chép file yêu cầu (requirements.txt) và cài đặt các thư viện
COPY requirements.txt .

# Cài đặt các thư viện trong requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép mã nguồn ứng dụng vào container
COPY . .

# Chạy ứng dụng
CMD ["python", "api.py"]
