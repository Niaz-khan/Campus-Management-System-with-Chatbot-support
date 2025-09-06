from django.apps import AppConfig

class LibraryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'library'

    def ready(self):
        # import signals or ensure tasks module is importable
        try:
            import library.signals  # optional if you add signals
        except Exception:
            pass
