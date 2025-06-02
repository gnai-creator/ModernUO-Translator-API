FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY translator_service.py .

EXPOSE 8100

CMD ["uvicorn", "translator_service:app", "--host", "0.0.0.0", "--port", "8100"]
