FROM python:3.11-slim

WORKDIR /app

COPY ./backend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["fastapi", "run"]