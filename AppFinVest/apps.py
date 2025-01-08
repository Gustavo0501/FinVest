from django.apps import AppConfig

class AppfinvestConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'AppFinVest'

    def ready(self):
        from .scheduler import start_scheduler
        start_scheduler()