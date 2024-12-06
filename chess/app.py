from django.apps import AppConfig

class YourAppConfig(AppConfig):
    name = 'yourapp'

    def ready(self):
        import chess.signals  # Ensure your signals are registered
        print("Ok")
