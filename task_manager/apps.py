from django.apps import AppConfig
from django.conf import settings


class TaskManagerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "task_manager"


def cfg_assets_root(request):
    return {"ASSETS_ROOT": settings.ASSETS_ROOT}
