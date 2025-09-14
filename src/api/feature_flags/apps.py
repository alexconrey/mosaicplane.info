from django.apps import AppConfig


class FeatureFlagsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'feature_flags'

    def ready(self):
        """Import signals when Django starts"""
        import feature_flags.signals
