# habits/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HabitViewSet

app_name = 'habits'  # ← Убедись, что это есть!

router = DefaultRouter()
router.register(r'habits', HabitViewSet, basename='habit')

urlpatterns = [
    path('', include(router.urls)),
    path('public/', HabitViewSet.as_view({'get': 'public'}), name='habit-public'),

]