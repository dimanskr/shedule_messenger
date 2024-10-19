from django.apps import AppConfig
from django.utils.autoreload import autoreload_started


class MailingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "mailing"

    def ready(self):
        # Запускаем планировщик только один раз, когда проект загружается
        autoreload_started.connect(self.start_scheduler)

    @staticmethod
    def start_scheduler(*args, **kwargs):
        """
        Метод для старта планировщика.
        """
        from .scheduler import start
        start()
