# habits/models.py
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from .validators import validate_duration, validate_periodicity


class Habit(models.Model):
    """
    Модель привычки

    Правила валидации:
    1. Нельзя одновременно заполнять related_habit и reward
    2. duration не может быть больше 120 секунд
    3. related_habit может быть только приятной привычкой
    4. У приятной привычки не может быть reward и related_habit
    5. periodicity от 1 до 7 дней
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='habits',
        verbose_name='Пользователь'
    )

    place = models.CharField(
        max_length=255,
        verbose_name='Место',
        help_text='Где выполнять привычку?'
    )

    time = models.TimeField(
        verbose_name='Время',
        help_text='Во сколько выполнять привычку?'
    )

    action = models.CharField(
        max_length=255,
        verbose_name='Действие',
        help_text='Что нужно сделать?'
    )

    is_pleasant = models.BooleanField(
        default=False,
        verbose_name='Приятная привычка',
        help_text='Отметьте, если это приятная привычка (награда)'
    )

    related_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Связанная привычка',
        help_text='Привычка, которая будет наградой (только для полезных привычек)'
    )

    periodicity = models.PositiveSmallIntegerField(
        validators=[validate_periodicity],
        default=1,
        verbose_name='Периодичность (дни)',
        help_text='Как часто выполнять привычку (от 1 до 7 дней)'
    )

    reward = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Вознаграждение',
        help_text='Чем себя вознаградить после выполнения'
    )

    duration = models.PositiveSmallIntegerField(
        validators=[validate_duration],
        verbose_name='Время на выполнение (сек)',
        help_text='Сколько времени займет выполнение (не более 120 секунд)'
    )

    is_public = models.BooleanField(
        default=False,
        verbose_name='Публичная',
        help_text='Отметьте, если привычка доступна всем'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.action} в {self.place} в {self.time}"

    def clean(self):
        """
        Комплексная валидация на уровне модели
        Вызывается при сохранении через form или serializer
        """
        # Правило 1: Нельзя одновременно выбрать related_habit и reward
        if self.related_habit and self.reward:
            raise ValidationError(
                'Нельзя одновременно указывать связанную привычку и вознаграждение'
            )

        # Правило 2: У приятной привычки не может быть reward и related_habit
        if self.is_pleasant:
            if self.reward or self.related_habit:
                raise ValidationError(
                    'У приятной привычки не может быть вознаграждения или связанной привычки'
                )

        # Правило 3: related_habit может быть только приятной привычкой
        if self.related_habit and not self.related_habit.is_pleasant:
            raise ValidationError(
                'Связанная привычка должна быть приятной'
            )

    def save(self, *args, **kwargs):
        # Вызываем валидацию перед сохранением
        self.full_clean()
        super().save(*args, **kwargs)
