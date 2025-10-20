#!/bin/sh

# Применяем миграции
python manage.py migrate

# Запускаем сбор статики
python manage.py collectstatic --noinput

# Запускаем переданную команду (например, gunicorn)
exec "$@"
