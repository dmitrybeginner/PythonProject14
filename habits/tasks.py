from celery import shared_task
import requests
from django.utils import timezone
from .models import Habit
from config.settings import TELEGRAM_BOT_TOKEN


@shared_task
def send_habit_reminder(habit_id):
    """
    Задача для отправки напоминания о привычке в Telegram.
    """
    try:
        habit = Habit.objects.get(id=habit_id)
        user = habit.user

        # Проверяем, что у пользователя есть связанный профиль и chat_id
        if hasattr(user, 'profile') and user.profile.telegram_chat_id:
            chat_id = user.profile.telegram_chat_id
            message = (
                f"Напоминание о привычке: Пора {habit.action} в {habit.place}. "
                f"Время выполнения: {habit.duration} секунд."
            )

            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            data = {"chat_id": chat_id, "text": message}
            response = requests.post(url, data=data)

            if response.status_code == 200:
                print(f"Напоминание для {user.username} отправлено успешно.")
            else:
                print(f"Ошибка отправки напоминания для {user.username}: {response.text}")
        else:
            print(f"Не удалось отправить напоминание: у пользователя {user.username} не привязан Telegram.")

    except Habit.DoesNotExist:
        print(f"Привычка с ID {habit_id} не найдена.")
    except Exception as e:
        print(f"Произошла ошибка при отправке напоминания для привычки {habit_id}: {e}")


@shared_task
def check_and_send_reminders():
    """
    Периодическая задача для проверки и отправки напоминаний.
    """
    now = timezone.now()
    # Фильтруем привычки, у которых подошло время
    habits_to_remind = Habit.objects.filter(
        time__hour=now.hour,
        time__minute=now.minute
    )

    for habit in habits_to_remind:
        # Проверяем, наступил ли день для напоминания согласно периодичности
        days_since_creation = (now.date() - habit.created_at.date()).days
        if days_since_creation % habit.frequency == 0:
            send_habit_reminder.delay(habit.id)
