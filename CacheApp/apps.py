from django.apps import AppConfig


class CacheappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'CacheApp'

    def ready(self):
        import CacheApp.signals
