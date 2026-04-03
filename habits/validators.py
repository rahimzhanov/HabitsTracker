# habits/validators.py
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_duration(value):
    """
    Проверяет, что время выполнения не больше 120 секунд
    """
    if value > 120:
        raise ValidationError(
            _('Время выполнения не может превышать 120 секунд (2 минуты)'),
            code='duration_too_long'
        )


def validate_periodicity(value):
    """
    Проверяет, что периодичность от 1 до 7 дней
    """
    if value < 1 or value > 7:
        raise ValidationError(
            _('Периодичность должна быть от 1 до 7 дней'),
            code='periodicity_invalid'
        )