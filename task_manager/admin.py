from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from task_manager.models import Task, Project, Worker, TaskType, Position


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_filter = ("is_completed",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_filter = ("is_completed",)


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position",)
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("position",)}),)
    )


admin.site.register(TaskType)
admin.site.register(Position)

admin.site.unregister(Group)
