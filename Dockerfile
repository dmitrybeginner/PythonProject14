# 1. Базовый образ
FROM python:3.10-slim

# 2. Установка переменных окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Установка рабочей директории
WORKDIR /app

# 4. Установка Poetry
RUN pip install poetry

# 5. Копирование файлов зависимостей и их установка
COPY poetry.lock pyproject.toml /app/
RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi

# 6. Копирование кода проекта
COPY . /app/

# 7. Копирование и установка прав для entrypoint
COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

# 8. Открытие порта
EXPOSE 8000

# 9. Установка entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

# 10. Команда для запуска (будет передана в entrypoint)
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]