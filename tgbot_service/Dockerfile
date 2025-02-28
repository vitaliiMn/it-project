FROM python:3.11-slim

WORKDIR /root

COPY requirements.txt /root/

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]