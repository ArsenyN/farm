from django.apps import AppConfig
# from farm_instance.tasks import add


class FarmBaseConfig(AppConfig):
    name = "farm_base"
    verbose_name = "SteamFarm Base"

    # def ready(self):
    #     # a = add.delay(1, 2)
    #     print("ready", a, 1)
