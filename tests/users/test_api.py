from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User


class UserAPITest(APITestCase):
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
