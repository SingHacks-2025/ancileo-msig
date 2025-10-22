FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY webhook/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY webhook/stripe_webhook.py .

EXPOSE 8085

CMD ["python", "stripe_webhook.py"]

