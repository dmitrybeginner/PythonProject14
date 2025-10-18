from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from habits.models import Habit
from habits.serializers import HabitSerializer


class HabitSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.pleasant_habit = Habit.objects.create(
            user=self.user,
            action="Пить чай",
            time="08:00:00",
            place="Кухня",
            duration=100,
            is_pleasant=True
        )
        self.base_data = {
            'user': self.user.pk,
            'action': 'Test Action',
            'time': '08:00:00',
            'place': 'Test Place',
            'duration': 60,
            'frequency': 1,
        }

    def test_reward_and_related_habit_validation(self):
        """Тест: нельзя одновременно указать вознаграждение и связанную привычку."""
        data = self.base_data.copy()
        data['reward'] = "Конфета"
        data['related_habit'] = self.pleasant_habit.pk
        serializer = HabitSerializer(data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_duration_validation(self):
        """Тест: время выполнения не должно превышать 120 секунд."""
        data = self.base_data.copy()
        data['duration'] = 121
        serializer = HabitSerializer(data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_related_habit_is_pleasant_validation(self):
        """Тест: в связанные привычки могут попадать только приятные привычки."""
        unpleasant_habit = Habit.objects.create(
            user=self.user, action="Test Unpleasant", time="09:00", place="Test", duration=60, is_pleasant=False
        )
        data = self.base_data.copy()
        data['related_habit'] = unpleasant_habit.pk
        serializer = HabitSerializer(data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_pleasant_habit_constraints_validation(self):
        """Тест: у приятной привычки не может быть вознаграждения или связанной привычки."""
        data = self.base_data.copy()
        data['is_pleasant'] = True
        data['reward'] = "Конфета"
        serializer = HabitSerializer(data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

        data = self.base_data.copy()
        data['is_pleasant'] = True
        data['related_habit'] = self.pleasant_habit.pk
        serializer = HabitSerializer(data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_frequency_validation(self):
        """Тест: периодичность должна быть от 1 до 7 дней."""
        data = self.base_data.copy()
        data['frequency'] = 8
        serializer = HabitSerializer(data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

        data['frequency'] = 0
        serializer = HabitSerializer(data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
