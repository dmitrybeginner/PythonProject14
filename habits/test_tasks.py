from unittest.mock import patch, MagicMock
from django.test import TestCase
from django.contrib.auth.models import User
import datetime

from .models import Habit
from .tasks import send_habit_reminder, check_and_send_reminders


class TaskTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        # Profile is created by a signal, we just need to retrieve and update it
        self.profile = self.user.profile
        self.profile.telegram_chat_id = 123456789
        self.profile.save()

        self.habit = Habit.objects.create(
            user=self.user,
            action="Тестовая привычка",
            time="12:00:00",
            place="Тестовое место",
            duration=60
        )

    @patch('habits.tasks.requests.post')
    def test_send_habit_reminder(self, mock_post):
        """Тестирование задачи по отправке напоминания."""
        # Мокируем ответ от API Telegram, чтобы он был успешным
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        # Вызываем задачу
        send_habit_reminder(self.habit.id)

        # Проверяем, что запрос к Telegram был сделан 1 раз
        mock_post.assert_called_once()

        # Проверяем, что chat_id и текст сообщения верны
        args, kwargs = mock_post.call_args
        self.assertIn('data', kwargs)
        self.assertEqual(kwargs['data']['chat_id'], self.profile.telegram_chat_id)
        self.assertIn(self.habit.action, kwargs['data']['text'])

    @patch('habits.tasks.send_habit_reminder.delay')
    @patch('habits.tasks.timezone.now')
    def test_check_and_send_reminders(self, mock_now, mock_delay):
        """Тестирование периодической задачи по проверке и отправке напоминаний."""
        # Устанавливаем "текущее" время равным времени нашей привычки
        mock_time = datetime.datetime(2023, 1, 1, 12, 0, 0, tzinfo=datetime.timezone.utc)
        mock_now.return_value = mock_time

        # Создаем еще одну привычку на другое время, чтобы убедиться, что вызывается только нужная
        Habit.objects.create(
            user=self.user,
            action="Другая привычка",
            time="13:00:00",
            place="Другое место",
            duration=60
        )

        # Вызываем основную периодическую задачу
        check_and_send_reminders()

        # Проверяем, что задача по отправке напоминания была вызвана ровно 1 раз
        mock_delay.assert_called_once()
        # Проверяем, что она была вызвана с ID именно нашей привычки
        mock_delay.assert_called_with(self.habit.id)
