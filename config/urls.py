# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from habits.views import telegram_webhook

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('habits.urls')),
    path('api/users/', include('users.urls')),
    path('telegram/webhook/', telegram_webhook, name='telegram-webhook'),
]

# В режиме разработки Django сам будет отдавать медиа-файлы
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
