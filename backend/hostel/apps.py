from django.apps import AppConfig

class HostelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hostel'

    def ready(self):
        # import signals if you add them
        try:
            import hostel.signals
        except Exception:
            pass
