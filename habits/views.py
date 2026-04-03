# habits/views.py
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.views import APIView

from .models import Habit
from .serializers import HabitSerializer
from .permissions import IsOwner
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse
import json
from .telegram import send_telegram_message
from users.models import User
from .tasks import send_due_habit_reminders


class SendRemindersView(APIView):
    """
    Ручной запуск отправки напоминаний (для тестирования)
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        result = send_due_habit_reminders.delay()
        return Response(
            {'task_id': result.id, 'message': 'Задача отправлена'},
            status=status.HTTP_202_ACCEPTED
        )


class HabitViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с привычками

    Права доступа:
    - Создание: только авторизованные
    - Просмотр своих: только авторизованные
    - Просмотр публичных: все авторизованные
    - Редактирование/удаление: только владелец
    """
    serializer_class = HabitSerializer

    # Фильтрация и поиск
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['action', 'place']
    ordering_fields = ['time', 'created_at', 'periodicity']
    ordering = ['-created_at']

    def get_queryset(self):
        """
        Возвращает список привычек в зависимости от запроса
        """
        if self.action == 'public':
            # Публичные привычки видны всем авторизованным
            return Habit.objects.filter(is_public=True)

        # Личные привычки - только свои
        return Habit.objects.filter(user=self.request.user)

    def get_permissions(self):
        """
        Настройка прав доступа для разных действий
        """
        if self.action in ['update', 'partial_update', 'destroy']:
            # Редактирование и удаление - только владелец
            permission_classes = [IsAuthenticated, IsOwner]
        else:
            # Остальные действия - просто авторизация
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """
        При создании привычки автоматически привязываем её к текущему пользователю
        """
        serializer.save(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        """
        Получение одной привычки с проверкой прав
        """
        habit = self.get_object()

        # Если привычка не публичная и не принадлежит пользователю - запрещаем
        if not habit.is_public and habit.user != request.user:
            return Response(
                {'error': 'У вас нет доступа к этой привычке'},
                status=status.HTTP_403_FORBIDDEN
            )

        return super().retrieve(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Удаление привычки с проверкой прав
        """
        habit = self.get_object()

        # Проверяем, что привычка принадлежит текущему пользователю
        if habit.user != request.user:
            return Response(
                {'error': 'Вы можете удалять только свои привычки'},
                status=status.HTTP_403_FORBIDDEN
            )

        return super().destroy(request, *args, **kwargs)

    def public(self, request):
        """
        Список публичных привычек (только для чтения)
        """
        queryset = Habit.objects.filter(is_public=True)

        # Применяем пагинацию
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


@csrf_exempt
@require_POST
def telegram_webhook(request):
    """
    Webhook для получения сообщений от Telegram
    Пользователь может отправить команду /start для привязки
    """
    try:
        data = json.loads(request.body)

        # Получаем информацию о сообщении
        message = data.get('message', {})
        chat_id = message.get('chat', {}).get('id')
        text = message.get('text', '')

        if text == '/start':
            # Пользователь запустил бота
            # Нужно вернуть ему инструкцию по привязке
            send_telegram_message(
                chat_id,
                "🤖 Привет! Я бот для напоминаний о привычках.\n\n"
                "Чтобы привязать аккаунт, перейдите в веб-приложение "
                "и введите ваш chat_id в настройках.\n\n"
                f"Ваш chat_id: <code>{chat_id}</code>"
            )

        return JsonResponse({'ok': True})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


class SendRemindersView(APIView):
    """
    Ручной запуск отправки напоминаний (для тестирования)
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        result = send_due_habit_reminders.delay()
        return Response(
            {'task_id': result.id, 'message': 'Задача отправлена'},
            status=status.HTTP_202_ACCEPTED
        )