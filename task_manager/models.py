from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class Position(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)


class TaskType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)


class Project(models.Model):
    name = models.CharField(max_length=255)
    is_completed = models.BooleanField(default=False, verbose_name="completed")

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("task_manager:project-detail", kwargs={"pk": self.pk})


class Task(models.Model):
    PRIORITY_CHOICES = [
        ("1", "URGENT"),
        ("2", "HIGH"),
        ("3", "NORMAL"),
        ("4", "LOW"),
        ("5", "MINOR"),
    ]

    name = models.CharField(max_length=255)
    description = models.CharField(max_length=2048)
    deadline = models.DateField(null=True, blank=True)
    is_completed = models.BooleanField(default=False, verbose_name="completed")
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES)
    task_type = models.ForeignKey(
        "TaskType", related_name="tasks", on_delete=models.PROTECT
    )
    project = models.ForeignKey(
        "Project", related_name="tasks", on_delete=models.CASCADE
    )
    assignees = models.ManyToManyField("Worker", related_name="tasks")

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("task_manager:task-detail", kwargs={"pk": self.pk})


class Worker(AbstractUser):
    position = models.ForeignKey(
        "Position",
        related_name="workers",
        null=True,
        on_delete=models.PROTECT,
    )

    class Meta:
        ordering = ["first_name", "last_name"]

    def __str__(self):
        return str(f"{self.username} ({self.first_name} {self.last_name})")

    def get_absolute_url(self):
        return reverse("task_manager:worker-detail", kwargs={"pk": self.pk})
