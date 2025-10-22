FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY payment_pages/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY payment_pages/app.py .

RUN mkdir -p static

EXPOSE 8085

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8085/health || exit 1

CMD ["python", "app.py"]

