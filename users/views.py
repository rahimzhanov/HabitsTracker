# users/views.py
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import UserRegistrationSerializer, UserSerializer
from .models import User
from habits.telegram import verify_telegram_bot, get_telegram_updates
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import User




class ConnectTelegramView(APIView):
    """
    Эндпоинт для привязки Telegram chat_id к пользователю
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Привязывает Telegram chat_id к текущему пользователю

        Ожидает: {"chat_id": "123456789"}
        """
        chat_id = request.data.get('chat_id')

        if not chat_id:
            return Response(
                {'error': 'Не указан chat_id'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = request.user
        user.telegram_chat_id = chat_id
        user.save()

        # Отправляем приветственное сообщение
        from habits.telegram import send_telegram_message
        send_telegram_message(
            chat_id,
            "✅ Вы успешно привязали аккаунт!\n\n"
            "Теперь вы будете получать напоминания о привычках."
        )

        return Response(
            {'message': 'Telegram успешно привязан', 'chat_id': chat_id},
            status=status.HTTP_200_OK
        )


class TelegramUpdatesView(APIView):
    """
    Просмотр обновлений Telegram (для получения chat_id)
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from habits.telegram import get_telegram_updates
        updates = get_telegram_updates()
        return Response(updates)


class RegisterView(generics.CreateAPIView):
    """Регистрация нового пользователя"""
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]  # Доступно всем

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Создаем токены для нового пользователя
        refresh = RefreshToken.for_user(user)

        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    """Вход в систему (получение токенов)"""
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)

        if user is None:
            return Response(
                {'error': 'Неверный email или пароль'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })