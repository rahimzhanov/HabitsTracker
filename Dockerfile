# Dockerfile
FROM python:3.13-slim

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Копируем requirements.txt и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Копируем весь проект
COPY . .

# Создаем директории для статики и медиа
RUN mkdir -p /app/staticfiles /app/media

# Собираем статику (будет выполнено при запуске через entrypoint)
# RUN python manage.py collectstatic --noinput

# Открываем порт
EXPOSE 8000

# Команда по умолчанию (будет переопределена в docker-compose)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]