from django.apps import AppConfig

class IngestConfig(AppConfig):
    name = 'ingest'
    verbose_name = 'Content Ingest'

    def ready(self):
        from . import signals