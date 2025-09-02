from django.apps import AppConfig

class SportsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sports'

    def ready(self):
        # import signals if you add any
        try:
            import sports.signals
        except Exception:
            pass
