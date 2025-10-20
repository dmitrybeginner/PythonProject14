
import re
import asyncio
from django.core.management.base import BaseCommand
from django.conf import settings
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from django.contrib.auth.models import User
from users.models import Profile  # Corrected import path

# Этапы диалога
EMAIL, TYPING_REPLY = range(2)

# Паттерн для проверки email
EMAIL_REGEX = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Начинает диалог при команде /start.
    Спрашивает у пользователя его email.
    """
    await update.message.reply_text(
        "Привет! Я бот для трекера привычек. Чтобы я мог присылать тебе напоминания, "
        "пожалуйста, введи email, который ты использовал при регистрации на сайте."
    )
    return EMAIL


async def received_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обрабатывает полученный email, связывает его с профилем пользователя.
    """
    chat_id = update.effective_chat.id
    email = update.message.text

    if not re.fullmatch(EMAIL_REGEX, email):
        await update.message.reply_text("Кажется, это не похоже на email. Попробуй еще раз.")
        return EMAIL

    try:
        user = await User.objects.aget(email=email)
        profile, created = await Profile.objects.aget_or_create(user=user)
        profile.telegram_chat_id = chat_id
        await profile.asave()
        await update.message.reply_text(
            "Отлично! Я связал твой Telegram с аккаунтом. Теперь ты будешь получать напоминания."
        )
        return ConversationHandler.END

    except User.DoesNotExist:
        await update.message.reply_text(
            "К сожалению, я не нашел пользователя с таким email. "
            "Убедись, что ты правильно ввел email, или зарегистрируйся на сайте."
        )
        return EMAIL


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Отменяет текущий диалог."""
    await update.message.reply_text("Действие отменено.")
    return ConversationHandler.END


class Command(BaseCommand):
    help = 'Запускает Telegram-бота для привязки аккаунтов пользователей.'

    def handle(self, *args, **options):
        if not settings.TELEGRAM_BOT_TOKEN:
            self.stdout.write(self.style.ERROR("Переменная окружения TELEGRAM_BOT_TOKEN не установлена."))
            return

        application = ApplicationBuilder().token(settings.TELEGRAM_BOT_TOKEN).build()

        conv_handler = ConversationHandler(
            entry_points=[CommandHandler("start", start)],
            states={
                EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, received_email)],
            },
            fallbacks=[CommandHandler("cancel", cancel)],
        )

        application.add_handler(conv_handler)

        self.stdout.write(self.style.SUCCESS("Бот запущен..."))

        # Используем asyncio.run() для запуска асинхронного приложения
        asyncio.run(application.run_polling())
