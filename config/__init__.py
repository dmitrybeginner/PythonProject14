import os
from celery import Celery

# Установить настройки Django для Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Создать экземпляр приложения Celery
celery_app = Celery('habits')

# Загрузить конфигурацию из настроек Django
# namespace='CELERY' означает, что все ключи конфигурации Celery должны иметь префикс CELERY_
celery_app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически обнаруживать задачи в файлах tasks.py приложений Django
celery_app.autodiscover_tasks()

__all__ = ('celery_app',)
