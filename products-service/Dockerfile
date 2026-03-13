FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN useradd --create-home appuser

COPY app.py .

USER appuser

EXPOSE 5002

CMD ["python", "app.py"]
