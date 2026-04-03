# habits/tests.py
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from habits.models import Habit

User = get_user_model()


class HabitModelTest(TestCase):
    """Тесты для модели Habit"""

    def setUp(self):
        self.user = User.objects.create_user(
            email='test@test.com',
            password='test123'
        )

    def test_create_valid_habit(self):
        habit = Habit.objects.create(
            user=self.user,
            place='Дома',
            time='08:00:00',
            action='Сделать зарядку',
            duration=60,
            periodicity=1,
            is_pleasant=False
        )
        self.assertEqual(habit.action, 'Сделать зарядку')
        self.assertEqual(habit.user.email, 'test@test.com')

    def test_duration_validation(self):
        habit = Habit(
            user=self.user,
            place='Дома',
            time='08:00:00',
            action='Сделать зарядку',
            duration=121,
            periodicity=1
        )
        with self.assertRaises(ValidationError):
            habit.full_clean()

    def test_periodicity_validation(self):
        habit = Habit(
            user=self.user,
            place='Дома',
            time='08:00:00',
            action='Сделать зарядку',
            duration=60,
            periodicity=0
        )
        with self.assertRaises(ValidationError):
            habit.full_clean()

    def test_pleasant_habit_no_reward(self):
        habit = Habit(
            user=self.user,
            place='Дома',
            time='08:00:00',
            action='Принять ванну',
            duration=60,
            periodicity=1,
            is_pleasant=True,
            reward='Шоколадка'
        )
        with self.assertRaises(ValidationError):
            habit.full_clean()


class HabitAPITest(TestCase):
    """Тесты API для привычек"""

    def setUp(self):
        self.client = APIClient()

        self.user1 = User.objects.create_user(
            email='user1@test.com',
            password='test123'
        )

        self.user2 = User.objects.create_user(
            email='user2@test.com',
            password='test123'
        )

        self.habit = Habit.objects.create(
            user=self.user1,
            place='Дома',
            time='08:00:00',
            action='Зарядка user1',
            duration=60,
            periodicity=1,
            is_public=True
        )

    def test_create_habit_unauthorized(self):
        """Тест: неавторизованный не может создать привычку"""
        # Используем app_name
        url = reverse('habits:habit-list')
        data = {
            'place': 'Спортзал',
            'time': '10:00:00',
            'action': 'Тренировка',
            'duration': 60,
            'periodicity': 1
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_habit_authorized(self):
        """Тест: авторизованный может создать привычку"""
        self.client.force_authenticate(user=self.user1)
        url = reverse('habits:habit-list')
        data = {
            'place': 'Спортзал',
            'time': '10:00:00',
            'action': 'Тренировка',
            'duration': 60,
            'periodicity': 1
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_own_habits(self):
        """Тест: пользователь видит только свои привычки"""
        self.client.force_authenticate(user=self.user1)
        url = reverse('habits:habit-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_user_can_see_public_habits(self):
        """Тест: пользователь видит публичные привычки других"""
        self.client.force_authenticate(user=self.user2)
        url = reverse('habits:habit-public')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Должен видеть публичную привычку user1
        self.assertEqual(len(response.data['results']), 1)

    def test_update_own_habit(self):
        """Тест: пользователь может редактировать свою привычку"""
        self.client.force_authenticate(user=self.user1)
        url = reverse('habits:habit-detail', args=[self.habit.id])
        data = {'action': 'Обновленная зарядка'}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.action, 'Обновленная зарядка')

    def test_cannot_update_others_habit(self):
        """Тест: пользователь не может редактировать чужую привычку"""
        self.client.force_authenticate(user=self.user2)
        url = reverse('habits:habit-detail', args=[self.habit.id])
        data = {'action': 'Попытка взлома'}
        response = self.client.patch(url, data)

        # Чужая привычка не доступна - ожидаем 404
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_own_habit(self):
        """Тест: пользователь может удалить свою привычку"""
        self.client.force_authenticate(user=self.user1)
        url = reverse('habits:habit-detail', args=[self.habit.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 0)

    def test_cannot_delete_others_habit(self):
        """Тест: пользователь не может удалить чужую привычку"""
        self.client.force_authenticate(user=self.user2)
        url = reverse('habits:habit-detail', args=[self.habit.id])
        response = self.client.delete(url)

        # Чужая привычка не доступна - ожидаем 404
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# Добавь в конец файла habits/tests.py

class HabitPermissionsTest(TestCase):
    """Тесты прав доступа"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='perm@test.com',
            password='test123'
        )
        self.habit = Habit.objects.create(
            user=self.user,
            place='Дома',
            time='08:00:00',
            action='Тест',
            duration=60,
            periodicity=1,
            is_public=True,
        )

    def test_is_owner_permission(self):
        """Тест: IsOwner разрешает доступ владельцу"""
        from habits.permissions import IsOwner
        from rest_framework.request import Request
        from django.test import RequestFactory

        factory = RequestFactory()
        request = factory.get('/')
        request.user = self.user

        permission = IsOwner()
        result = permission.has_object_permission(request, None, self.habit)
        self.assertTrue(result)

    def test_public_habit_readonly(self):
        """Тест: публичная привычка доступна для чтения другим"""
        self.client.force_authenticate(user=self.user)
        self.habit.is_public = True
        self.habit.save()

        url = reverse('habits:habit-detail', args=[self.habit.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_own_habit_permission(self):
        """Тест: удаление своей привычки"""
        self.client.force_authenticate(user=self.user)
        url = reverse('habits:habit-detail', args=[self.habit.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)