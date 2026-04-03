# config/celery.py
import os
from celery import Celery
from celery.schedules import crontab

# Устанавливаем настройки Django по умолчанию
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Создаем экземпляр Celery
app = Celery('config')

# Загружаем настройки из Django settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически находим задачи в приложениях
app.autodiscover_tasks()

# Настройка периодических задач (расписание)
app.conf.beat_schedule = {
    'send-habit-reminders': {
        'task': 'habits.tasks.send_due_habit_reminders',
        'schedule': crontab(minute='*/1'),  # Каждую минуту для теста
        # Потом изменим на crontab(minute='*', hour='8-22') - каждый час с 8 до 22
    },
}
