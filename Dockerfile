# Use an official lightweight Python image
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# Cloud Run injects the $PORT variable automatically
CMD exec gunicorn --bind :$PORT --workers 2 --threads 4 --timeout 0 app:app