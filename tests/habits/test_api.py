from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from habits.models import Habit


class HabitAPITest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1',
            password='pass1',
            email='user1@test.com'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='pass2'
        )
        self.habit1 = Habit.objects.create(
            user=self.user1,
            action='Спорт',
            time='06:00:00',
            place='Зал',
            duration=60
        )
        self.public_habit = Habit.objects.create(
            user=self.user2,
            action='Публичная',
            time='10:00:00',
            place='Улица',
            duration=45,
            is_public=True
        )

    def test_register_user(self):
        """Тест регистрации нового пользователя."""
        data = {
            'username': 'newuser',
            'password': 'newpass',
            'email': 'new@test.com'
        }
        response = self.client.post('/api/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_list_own_habits(self):
        """Тест получения списка своих привычек."""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get('/api/habits/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['action'], self.habit1.action)

    def test_list_public_habits(self):
        """Тест получения списка публичных привычек."""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get('/api/habits/public/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Пагинация была добавлена, поэтому проверяем 'results'
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['action'], self.public_habit.action)

    def test_habit_permissions(self):
        """Тест: пользователь не может видеть или изменять чужие привычки."""
        self.client.force_authenticate(user=self.user2)
        # Попытка получить доступ к чужой привычке
        response = self.client.get(f'/api/habits/{self.habit1.pk}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Попытка изменить чужую привычку
        response = self.client.patch(f'/api/habits/{self.habit1.pk}/', {'action': 'Новое действие'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Попытка удалить чужую привычку
        response = self.client.delete(f'/api/habits/{self.habit1.pk}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_habit_crud(self):
        """Тест полного CRUD-цикла для привычки."""
        self.client.force_authenticate(user=self.user1)

        # Create
        data = {'action': 'Читать книгу', 'time': '20:00:00', 'place': 'Кровать', 'duration': 30, 'user': self.user1.pk}
        response = self.client.post('/api/habits/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        habit_id = response.data['id']

        # Retrieve
        response = self.client.get(f'/api/habits/{habit_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['action'], 'Читать книгу')

        # Update
        update_data = {'duration': 45}
        response = self.client.patch(f'/api/habits/{habit_id}/', update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['duration'], 45)

        # Delete
        response = self.client.delete(f'/api/habits/{habit_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify deletion
        response = self.client.get(f'/api/habits/{habit_id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
