#!/bin/sh

# Даем время базе данных на полный запуск
sleep 10

# Применяем миграции
python manage.py migrate

# Запускаем сбор статики
python manage.py collectstatic --noinput

# Запускаем переданную команду (например, gunicorn)
exec "$@"
