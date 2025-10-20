from rest_framework.exceptions import ValidationError


class DurationValidator:
    """Проверяет, что время выполнения не превышает 120 секунд."""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        duration = value.get(self.field)
        if duration is not None and duration > 120:
            raise ValidationError("Время выполнения привычки не может превышать 120 секунд.")


class RewardAndRelatedHabitValidator:
    """Исключает одновременный выбор связанной привычки и вознаграждения."""

    def __call__(self, value):
        reward = value.get('reward')
        related_habit = value.get('related_habit')
        if reward and related_habit:
            raise ValidationError("Нельзя одновременно указывать вознаграждение и связанную привычку.")


class RelatedHabitIsPleasantValidator:
    """Проверяет, что связанная привычка является приятной."""

    def __call__(self, value):
        related_habit = value.get('related_habit')
        if related_habit and not related_habit.is_pleasant:
            raise ValidationError("В связанные привычки могут попадать только привычки с признаком приятной.")


class PleasantHabitValidator:
    """Проверяет, что у приятной привычки нет вознаграждения или связанной привычки."""

    def __call__(self, value):
        is_pleasant = value.get('is_pleasant')
        reward = value.get('reward')
        related_habit = value.get('related_habit')
        if is_pleasant and (reward or related_habit):
            raise ValidationError("У приятной привычки не может быть вознаграждения или связанной привычки.")


class FrequencyValidator:
    """Проверяет, что периодичность не реже 1 раза в 7 дней."""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        frequency = value.get(self.field)
        if frequency is not None and not (1 <= frequency <= 7):
            raise ValidationError("Нельзя выполнять привычку реже, чем 1 раз в 7 дней.")
