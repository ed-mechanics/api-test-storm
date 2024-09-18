FROM python:3.11.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Копируем конфигурацию Alembic
COPY alembic.ini .
COPY alembic alembic

RUN chmod +x start.sh

EXPOSE 8000

CMD ["./start.sh"]
