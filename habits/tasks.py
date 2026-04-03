# habits/tasks.py
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Habit
from .telegram import send_telegram_message


@shared_task
def send_habit_reminder(habit_id, user_telegram_id, habit_action, habit_place, habit_time):
    """
    Отправляет напоминание о конкретной привычке
    """
    message = f"""⏰ НАПОМИНАНИЕ О ПРИВЫЧКЕ!

Действие: {habit_action}
Место: {habit_place}
Время: {habit_time}

Не забудьте выполнить!"""

    result = send_telegram_message(user_telegram_id, message)
    return f"Отправлено {user_telegram_id}: {habit_action} - {result}"


@shared_task
def send_due_habit_reminders():
    """
    Находит все привычки, которые нужно выполнить сейчас,
    и отправляет напоминания
    """
    now = timezone.now()
    current_time = now.time()
    current_weekday = now.weekday()  # 0 = понедельник, 6 = воскресенье

    # Находим привычки, которые нужно выполнить сейчас
    # Условия:
    # 1. Привычка не приятная (полезная)
    # 2. Время выполнения совпадает с текущим (с точностью до минуты)
    # 3. Пользователь привязал Telegram
    # 4. Периодичность соответствует дню недели

    habits = Habit.objects.filter(
        is_pleasant=False,
        user__telegram_chat_id__isnull=False,  # У пользователя есть Telegram
    )

    sent_count = 0
    errors = []

    for habit in habits:
        # Проверяем, что время совпадает (с точностью до минуты)
        if habit.time.hour == current_time.hour and habit.time.minute == current_time.minute:
            # Проверяем периодичность
            # Если periodicity = 1 - каждый день
            # Если periodicity = 7 - раз в неделю
            # Упрощенно: проверяем, что день недели кратен periodicity
            if current_weekday % habit.periodicity == 0:
                # Отправляем напоминание
                send_habit_reminder.delay(
                    habit.id,
                    habit.user.telegram_chat_id,
                    habit.action,
                    habit.place,
                    habit.time.strftime('%H:%M')
                )
                sent_count += 1

    return {
        'status': 'completed',
        'sent': sent_count,
        'errors': errors
    }


@shared_task
def debug_task():
    """
    Тестовая задача для проверки работы Celery
    """
    print("✅ Celery работает!")
    return "Celery is working"