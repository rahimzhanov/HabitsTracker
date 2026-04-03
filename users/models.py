# users/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Кастомный менеджер для создания пользователей без username
    """

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Кастомная модель пользователя
    """
    username = None  # Убираем поле username
    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(max_length=35, blank=True, null=True, verbose_name='Телефон')
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name='Город')
    avatar = models.ImageField(upload_to='users/avatars/', blank=True, null=True, verbose_name='Аватар')

    # Поле для Telegram (понадобится в Этапе 7)
    telegram_chat_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Telegram ID',
        help_text='ID чата в Telegram для получения уведомлений'
    )

    USERNAME_FIELD = 'email'  # Вход по email
    REQUIRED_FIELDS = []  # Дополнительные поля не требуются

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email