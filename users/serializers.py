# users/serializers.py
from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра информации о пользователе"""

    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'city', 'avatar', 'telegram_chat_id']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации нового пользователя"""
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True, label='Подтверждение пароля')

    class Meta:
        model = User
        fields = ['email', 'password', 'password2', 'phone', 'city', 'avatar']

    def validate(self, attrs):
        """Проверяем, что пароли совпадают"""
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        return attrs

    def create(self, validated_data):
        """Создаем пользователя"""
        validated_data.pop('password2')
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            phone=validated_data.get('phone', ''),
            city=validated_data.get('city', ''),
            avatar=validated_data.get('avatar', None)
        )
        return user