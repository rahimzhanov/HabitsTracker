# habits/telegram.py
import requests
from django.conf import settings
from django.core.exceptions import ValidationError


def send_telegram_message(chat_id, message):
    """
    Отправляет сообщение пользователю в Telegram

    Аргументы:
        chat_id: ID чата пользователя в Telegram
        message: Текст сообщения

    Возвращает:
        True, если отправлено успешно, иначе False
    """
    if not chat_id:
        return False

    url = f"https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/sendMessage"

    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"Ошибка отправки Telegram: {e}")
        return False


def get_telegram_updates():
    """
    Получает обновления от Telegram (для получения chat_id)
    Используется для отладки
    """
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/getUpdates"

    try:
        response = requests.get(url, timeout=10)
        return response.json()
    except Exception as e:
        print(f"Ошибка получения обновлений: {e}")
        return None


def verify_telegram_bot():
    """
    Проверяет, что бот работает и токен правильный
    """
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/getMe"

    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                print(f"✅ Бот @{data['result']['username']} работает!")
                return True
    except Exception as e:
        print(f"❌ Ошибка: {e}")

    return False