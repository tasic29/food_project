from django.apps import AppConfig


class ShareFoodConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'share_food'

    def ready(self) -> None:
        import share_food.signals
