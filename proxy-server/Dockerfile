FROM python:3.13-slim
WORKDIR /app
COPY proxy-server/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY proxy-server/app.py .
COPY frontend frontend
EXPOSE 8000
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT:-8000}"]
