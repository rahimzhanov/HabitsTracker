# habits/serializers.py
from rest_framework import serializers
from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Habit

    Преобразует модель Habit в JSON и обратно
    """

    # Добавляем поле для отображения email владельца (только для чтения)
    owner_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Habit
        fields = [
            'id',
            'owner_email',  # Email владельца
            'place',  # Место выполнения
            'time',  # Время выполнения
            'action',  # Действие
            'is_pleasant',  # Приятная привычка?
            'related_habit',  # Связанная привычка
            'periodicity',  # Периодичность (дни)
            'reward',  # Вознаграждение
            'duration',  # Длительность (сек)
            'is_public',  # Публичная?
            'created_at',  # Дата создания
            'updated_at',  # Дата обновления
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'owner_email']

    def validate(self, data):
        """
        Дополнительная валидация на уровне сериализатора

        Здесь дублируем валидацию из модели для более понятных ошибок API
        """
        # Правило 1: Нельзя одновременно выбрать related_habit и reward
        if data.get('related_habit') and data.get('reward'):
            raise serializers.ValidationError(
                'Нельзя одновременно указывать связанную привычку и вознаграждение'
            )

        # Правило 2: У приятной привычки не может быть reward и related_habit
        if data.get('is_pleasant'):
            if data.get('reward') or data.get('related_habit'):
                raise serializers.ValidationError(
                    'У приятной привычки не может быть вознаграждения или связанной привычки'
                )

        # Правило 3: related_habit может быть только приятной привычкой
        related = data.get('related_habit')
        if related and not related.is_pleasant:
            raise serializers.ValidationError(
                'Связанная привычка должна быть приятной'
            )

        return data
