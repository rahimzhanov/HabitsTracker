# users/urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from .views import RegisterView, ConnectTelegramView, TelegramUpdatesView

app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

# Telegram endpoints
    path('telegram/connect/', ConnectTelegramView.as_view(), name='telegram-connect'),
    path('telegram/updates/', TelegramUpdatesView.as_view(), name='telegram-updates'),
]