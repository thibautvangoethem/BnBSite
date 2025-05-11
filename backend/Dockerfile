FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && python3 -m pip install -r requirements.txt --no-cache-dir

COPY . ./backend

EXPOSE 8000

CMD ["python", "./backend/main_docker.py"]