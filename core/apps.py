from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    # Remove any model imports from here
    # Don't override ready() unless absolutely necessary