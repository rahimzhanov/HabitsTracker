# habits/permissions.py
from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Разрешение: только владелец объекта

    Используется для проверки, что пользователь является владельцем привычки
    """

    def has_object_permission(self, request, view, obj):
        """
        Проверка прав на конкретный объект

        obj - объект привычки (Habit)
        """
        # Безопасные методы (GET, HEAD, OPTIONS) разрешаем всем авторизованным
        if request.method in permissions.SAFE_METHODS:
            return True

        # Для изменяющих методов (POST, PUT, DELETE) - только владелец
        return obj.user == request.user


class IsPublicReadOnly(permissions.BasePermission):
    """
    Разрешение: публичные привычки доступны только для чтения

    Пользователи могут просматривать чужие публичные привычки,
    но не могут их изменять или удалять
    """

    def has_object_permission(self, request, view, obj):
        # Для безопасных методов (GET) - разрешаем все публичные привычки
        if request.method in permissions.SAFE_METHODS:
            return True

        # Для изменения - только владелец (проверяем через IsOwner)
        return obj.user == request.user
