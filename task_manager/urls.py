from django.contrib.auth.views import logout_then_login
from django.urls import path, include

from task_manager import views
from task_manager.views import (
    TaskListView,
    TaskCreateView,
    TaskUpdateView,
    TaskDetailView,
    ProjectListView,
    ProjectDetailView,
    ProjectCreateView,
    ProjectUpdateView,
    WorkerListView,
    WorkerDetailView,
    WorkerCreateView,
    WorkerUpdateView,
    LoginView,
)

app_name = "task_manager"

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", logout_then_login, name="logout"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path(
        "tasks/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"
    ),
    path("tasks/<int:pk>/delete/", views.task_delete, name="task-delete"),
    path("projects/", ProjectListView.as_view(), name="project-list"),
    path(
        "projects/<int:pk>/",
        ProjectDetailView.as_view(),
        name="project-detail",
    ),
    path(
        "projects/create/", ProjectCreateView.as_view(), name="project-create"
    ),
    path(
        "projects/<int:pk>/update/",
        ProjectUpdateView.as_view(),
        name="project-update",
    ),
    path(
        "projects/<int:pk>/delete/",
        views.project_delete,
        name="project-delete",
    ),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path(
        "workers/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"
    ),
    path("workers/create/", WorkerCreateView.as_view(), name="worker-create"),
    path(
        "workers/<int:pk>/update/",
        WorkerUpdateView.as_view(),
        name="worker-update",
    ),
    path(
        "workers/<int:pk>/delete/", views.worker_delete, name="worker-delete"
    ),
]
