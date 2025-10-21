# Трекер полезных привычек

Бэкенд-часть SPA веб-приложения для трекера полезных привычек на основе книги Джеймса Клира "Атомные привычки".

## Описание проекта

Приложение позволяет пользователям создавать, отслеживать и управлять своими полезными привычками. Включает интеграцию с Telegram для напоминаний и асинхронную обработку задач через Celery.

## Основные возможности

- **Регистрация и авторизация пользователей** через JWT-токены
- **Создание и управление привычками** (CRUD операции)
- **Пагинация** списков привычек (по 5 на страницу)
- **Валидация данных** привычек согласно бизнес-правилам
- **Права доступа** (пользователи видят только свои привычки, публичные доступны всем)
- **Интеграция с Telegram** для привязки аккаунтов и получения напоминаний
- **Асинхронные задачи** через Celery для отправки напоминаний
- **API документация** через Swagger/ReDoc

## Критерии приемки

- ✅ Настроен CORS
- ✅ Интеграция с Telegram
- ✅ Пагинация (5 привычек на страницу)
- ✅ Переменные окружения
- ✅ Модели Habit и Profile
- ✅ Все необходимые эндпоинты
- ✅ Валидаторы на уровне модели и сериализатора
- ✅ Права доступа (IsAuthenticated, IsOwner, AllowAny)
- ✅ Отложенные задачи через Celery
- ✅ Покрытие тестами >80% (87%)
- ✅ Код соответствует лучшим практикам
- ✅ Зависимости через Poetry
- ✅ Flake8 100% (исключая миграции)
- ✅ Выложено на GitHub

## Модели данных

### Привычка (Habit)
- Пользователь (создатель)
- Место выполнения
- Время выполнения
- Действие
- Признак приятной привычки
- Связанная привычка (для вознаграждения)
- Периодичность (1-7 дней)
- Вознаграждение (текст)
- Время на выполнение (≤120 сек)
- Признак публичности

### Профиль (Profile)
- Расширение модели User для хранения telegram_chat_id

## Валидаторы

- Одновременный выбор связанной привычки и вознаграждения запрещен
- Время выполнения ≤ 120 секунд
- Связанные привычки только с признаком "приятная"
- У приятных привычек нет вознаграждения/связи
- Периодичность 1-7 дней

## Эндпоинты API

- `POST /api/register/` - Регистрация пользователя
- `POST /api/token/` - Получение JWT-токена
- `POST /api/token/refresh/` - Обновление токена
- `GET/POST /api/habits/` - Список привычек пользователя / Создание привычки
- `GET/PUT/PATCH/DELETE /api/habits/{id}/` - Детали привычки
- `GET /api/habits/public/` - Публичные привычки

## Установка и запуск

### Требования
- Python 3.10+
- Poetry
- PostgreSQL
- Redis
- Telegram Bot Token

### Вариант 1: Docker Compose (рекомендуется)
1. Установите Docker и Docker Compose
2. Клонируйте репозиторий: `git clone <url>`
3. Перейдите в директорию: `cd pythonproject14`
4. Создайте файл `.env` с переменной `TELEGRAM_BOT_TOKEN=your_bot_token`
5. Запустите: `docker-compose up --build`
6. Приложение будет доступно на http://localhost:8000

### Вариант 2: Ручная установка
#### Установка PostgreSQL
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install postgresql postgresql-contrib

# Создание пользователя и БД
sudo -u postgres psql
CREATE USER habits_user WITH PASSWORD 'habits_password';
CREATE DATABASE habits_db OWNER habits_user;
GRANT ALL PRIVILEGES ON DATABASE habits_db TO habits_user;
\q
```

#### Установка Redis
```bash
# Ubuntu/Debian
sudo apt install redis-server
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

#### Настройка проекта
1. Установите Poetry: `pip install poetry`
2. Клонируйте репозиторий: `git clone <url>`
3. Перейдите в директорию: `cd pythonproject14`
4. Установите зависимости: `poetry install`

#### Настройка переменных окружения
1. Создайте файл `.env`:
   ```
   SECRET_KEY=your_secret_key_here
   DEBUG=True
   DB_NAME=habits_db
   DB_USER=habits_user
   DB_PASSWORD=habits_password
   DB_HOST=localhost
   DB_PORT=5432
   REDIS_URL=redis://127.0.0.1:6379
   TELEGRAM_BOT_TOKEN=your_bot_token
   ```

2. Выполните миграции: `poetry run python manage.py migrate`

### Запуск
1. Сервер: `poetry run python manage.py runserver`
2. Celery Worker: `poetry run celery -A config worker -l INFO`
3. Celery Beat: `poetry run celery -A config beat -l INFO`
4. Telegram Bot: `poetry run python manage.py run_telegram_bot`

## API Документация

- **Swagger UI**: http://localhost:8000/swagger/
- **ReDoc**: http://localhost:8000/redoc/

## Тестирование

- Запуск тестов: `poetry run python manage.py test`
- Покрытие: `coverage run --source='.' manage.py test && coverage report`
- Линтинг: `flake8 --max-line-length=120 --exclude=migrations`

## Интеграция с Telegram

1. Создайте бота через @BotFather в Telegram
2. Получите токен и добавьте в `.env`
3. Запустите команду `run_telegram_bot`
4. Пользователи пишут `/start` боту и вводят email для привязки аккаунта
5. После привязки бот будет отправлять напоминания о привычках

## Архитектура

- **Backend**: Django + DRF
- **Асинхронные задачи**: Celery + Redis
- **Документация**: drf-yasg (Swagger/ReDoc)
- **Управление зависимостями**: Poetry
- **Линтинг**: Flake8
- **Тестирование**: coverage

## Безопасность

- JWT-аутентификация
- CORS настроен для фронтенда
- Переменные окружения для секретов
- Права доступа на уровне представлений

