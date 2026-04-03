# Трекер полезных привычек

## Описание проекта

Backend-приложение для отслеживания и управления полезными привычками. Пользователи могут создавать привычки, получать напоминания в Telegram и следить за своим прогрессом.

## Функциональность

- Регистрация и авторизация пользователей (JWT)
- Создание, редактирование и удаление привычек
- Публичные привычки (доступны для просмотра другим пользователям)
- Интеграция с Telegram для напоминаний
- Автоматические уведомления о необходимости выполнить привычку
- Пагинация (5 привычек на странице)
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
- Swagger/ReDoc (документация API)
- CORS (для фронтенда)

## Установка и запуск

### 1. Клонирование репозитория

git clone https://github.com/rahimzhanov/habits-tracker.git
cd habits-tracker

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

python manage.py makemigrations
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

## API Эндпоинты

### Пользователи

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| POST | /api/users/register/ | Регистрация |
| POST | /api/users/login/ | Вход (получение токена) |
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

- Swagger UI: http://127.0.0.1:8000/swagger/
- ReDoc: http://127.0.0.1:8000/redoc/

## Структура проекта
```commandline


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
├── media/                  # Загружаемые файлы
├── static/                 # Статические файлы
├── .env                    # Переменные окружения
├── .gitignore
├── manage.py
└── requirements.txt
```
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