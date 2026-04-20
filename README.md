# Трекер полезных привычек

## Описание проекта

Backend-приложение для отслеживания и управления полезными привычками. Пользователи могут создавать привычки, получать напоминания в Telegram и следить за своим прогрессом.

Проект полностью контейнеризирован и может быть запущен через Docker Compose. Настроен CI/CD с использованием GitHub Actions для автоматического тестирования и деплоя на удаленный сервер.

## Адрес развернутого приложения

Сервер доступен по адресу:
http://81.26.181.203:8080/api/habits/

## Функциональность

- Регистрация и авторизация пользователей (JWT)
- Создание, редактирование и удаление привычек
- Публичные привычки (доступны для просмотра другим пользователям)
- Интеграция с Telegram для напоминаний
- Автоматические уведомления о необходимости выполнить привычку
- Пагинация (5 привычек на страницу)
- Валидация данных:
  - Длительность выполнения не более 120 секунд
  - Периодичность от 1 до 7 дней
  - Нельзя одновременно указать вознаграждение и связанную привычку
  - Связанная привычка должна быть приятной
  - У приятной привычки не может быть вознаграждения

## Технологии

- Python 3.13
- Django 6.0.3
- Django REST Framework 3.17.1
- JWT аутентификация
- PostgreSQL
- Redis (брокер сообщений)
- Celery (отложенные задачи)
- Celery Beat (периодические задачи)
- Telegram Bot API
- Docker / Docker Compose
- GitHub Actions (CI/CD)
- Nginx (веб-сервер)
- Gunicorn (WSGI сервер)

## Установка и запуск (локально)

### 1. Клонирование репозитория

git clone https://github.com/rahimzhanov/HabitsTracker.git
cd HabitsTracker

### 2. Создание виртуального окружения

python -m venv venv
venv\Scripts\activate  # для Windows
source venv/bin/activate  # для Mac/Linux

### 3. Установка зависимостей

pip install -r requirements.txt

### 4. Настройка переменных окружения

Создайте файл .env в корне проекта:

SECRET_KEY=your-secret-key-here
DEBUG=True

# База данных
DATABASE_NAME=habits_db
DATABASE_USER=postgres
DATABASE_PASSWORD=your_password
DATABASE_HOST=localhost
DATABASE_PORT=5432

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# Telegram
TELEGRAM_TOKEN=your_telegram_bot_token

### 5. Создание базы данных

В PostgreSQL:
CREATE DATABASE habits_db;

### 6. Применение миграций

python manage.py migrate

### 7. Создание суперпользователя

python manage.py createsuperuser

### 8. Запуск Redis

redis-server

### 9. Запуск Celery Worker (в отдельном терминале)

celery -A config worker --loglevel=info --pool=solo

### 10. Запуск Celery Beat (в отдельном терминале)

celery -A config beat --loglevel=info

### 11. Запуск Django сервера

python manage.py runserver

## Запуск через Docker (рекомендуемый способ)

### 1. Установите Docker и Docker Compose

### 2. Склонируйте репозиторий

git clone https://github.com/rahimzhanov/HabitsTracker.git
cd HabitsTracker

### 3. Запустите проект

docker-compose up --build

### 4. Проект будет доступен по адресу

http://localhost:8080/api/habits/

## API Эндпоинты

### Пользователи

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| POST | /api/users/register/ | Регистрация |
| POST | /api/users/token/ | Вход (получение токена) |
| POST | /api/users/token/refresh/ | Обновление токена |
| POST | /api/users/telegram/connect/ | Привязка Telegram chat_id |

### Привычки

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| GET | /api/habits/ | Список своих привычек |
| POST | /api/habits/ | Создание привычки |
| GET | /api/habits/{id}/ | Детали привычки |
| PUT | /api/habits/{id}/ | Полное обновление |
| PATCH | /api/habits/{id}/ | Частичное обновление |
| DELETE | /api/habits/{id}/ | Удаление |
| GET | /api/habits/public/ | Список публичных привычек |

## Документация API

- Swagger UI: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/

## Структура проекта
````
HabitsTracker/
├── config/                 # Настройки проекта
│   ├── __init__.py
│   ├── celery.py          # Celery настройки
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── habits/                 # Приложение привычек
│   ├── migrations/        # Миграции БД
│   ├── __init__.py
│   ├── admin.py
│   ├── models.py          # Модель Habit
│   ├── permissions.py     # IsOwner permission
│   ├── serializers.py     # HabitSerializer
│   ├── tasks.py           # Celery задачи
│   ├── telegram.py        # Telegram бот
│   ├── tests.py           # Тесты
│   ├── urls.py
│   ├── validators.py      # Валидаторы
│   └── views.py           # HabitViewSet
├── users/                  # Приложение пользователей
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── models.py          # Модель User (с telegram_chat_id)
│   ├── serializers.py     # Регистрация
│   ├── urls.py
│   └── views.py           # RegisterView, LoginView
├── nginx/                  # Конфигурация Nginx
│   └── nginx.conf
├── media/                  # Загружаемые файлы
├── static/                 # Статические файлы
├── Dockerfile
├── docker-compose.yml
├── .env                    # Переменные окружения
├── .gitignore
├── manage.py
└── requirements.txt
````
## CI/CD (GitHub Actions)

Проект настроен на автоматическое тестирование и деплой при каждом push в ветку main.

### Этапы CI/CD:

1. Установка зависимостей
2. Линтинг кода (flake8)
3. Запуск тестов
4. Сборка Docker образов
5. Деплой на удаленный сервер через SSH

### Secrets для GitHub Actions:

| Secret | Описание |
|--------|----------|
| SERVER_HOST | IP адрес сервера (81.26.181.203) |
| SERVER_USER | Имя пользователя на сервере (ubuntu) |
| SSH_PRIVATE_KEY | Приватный SSH ключ для доступа к серверу |

## Настройка удаленного сервера

### 1. Установите Docker и Docker Compose на сервер

sudo apt update
sudo apt install docker.io docker-compose -y
sudo usermod -aG docker $USER

### 2. Создайте директорию для проекта

sudo mkdir -p /var/www/habits-tracker

### 3. GitHub Actions автоматически скопирует код и запустит контейнеры

### 4. Проект будет доступен по адресу

http://81.26.181.203:8080/api/habits/

## Тестирование

Запуск всех тестов:
python manage.py test

Запуск с покрытием:
coverage run manage.py test
coverage report

## Telegram бот

1. Создайте бота через @BotFather в Telegram
2. Получите токен и добавьте в .env
3. Найдите свой chat_id:
   - Напишите боту /start
   - Откройте: https://api.telegram.org/bot<ТОКЕН>/getUpdates
4. Привяжите chat_id через API: POST /api/users/telegram/connect/

## Права доступа

- Пользователи видят только свои привычки
- Публичные привычки доступны всем авторизованным пользователям (только чтение)
- Редактирование/удаление - только владелец

## Автор

Аман Рахимжанов

## Лицензия

MIT