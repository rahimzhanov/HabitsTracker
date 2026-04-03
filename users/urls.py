# users/urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, LoginView, ConnectTelegramView, TelegramUpdatesView

app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

# Telegram endpoints
    path('telegram/connect/', ConnectTelegramView.as_view(), name='telegram-connect'),
    path('telegram/updates/', TelegramUpdatesView.as_view(), name='telegram-updates'),
]