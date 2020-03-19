from django.apps import AppConfig

class ActivityAppConfig(AppConfig):
    name = 'c2shiptrack'

    def ready(self):
        import c2shiptrack.signals
