from rest_framework import serializers
from .models import Habit
from .validators import (
    DurationValidator,
    FrequencyValidator,
    PleasantHabitValidator,
    RelatedHabitIsPleasantValidator,
    RewardAndRelatedHabitValidator
)


class HabitSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Habit.
    Включает валидацию на уровне полей и на уровне всего объекта.
    """
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Habit
        fields = '__all__'
        validators = [
            # Валидаторы уровня объекта
            RewardAndRelatedHabitValidator(),
            RelatedHabitIsPleasantValidator(),
            PleasantHabitValidator(),
            # Валидаторы, которые технически являются валидаторами полей,
            # но для работы им нужен доступ ко всему словарю данных.
            DurationValidator(field='duration'),
            FrequencyValidator(field='frequency'),
        ]
