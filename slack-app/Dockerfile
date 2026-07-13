FROM python:3.11-slim

WORKDIR /app/slack-app
COPY slack-app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY slack-app ./
ENV PYTHONPATH=/app/slack-app

CMD ["python", "app.py"]
