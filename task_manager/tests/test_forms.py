from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.models import Position, Worker, TaskType, Project, Task


class CreateFormTests(TestCase):
    def setUp(self):
        position = Position.objects.create(name="test position")
        TaskType.objects.create(name="task type name")
        Project.objects.create(name="project name")
        self.user = Worker.objects.create_user(
            username="test2",
            password="1qazcde3",
            position=position,
        )
        self.client.force_login(self.user)

    def test_task_create_form(self):
        name = "task name"
        description = "task description"
        deadline = "2020-05-25"
        is_completed = False
        form_data = {
            "name": name,
            "description": description,
            "deadline": deadline,
            "is_completed": is_completed,
            "priority": 1,
            "task_type": 1,
            "project": 1,
            "assignees": [1],
        }
        self.client.post(reverse("task_manager:task-create"), data=form_data)
        task = Task.objects.get(name=name)

        self.assertEqual(task.name, name)
        self.assertEqual(task.description, description)
        self.assertEqual(str(task.deadline), deadline)
        self.assertEqual(task.is_completed, is_completed)

    def test_project_create_form(self):
        name = "project 12345"
        is_completed = False
        form_data = {
            "name": name,
            "is_completed": is_completed,
        }
        self.client.post(
            reverse("task_manager:project-create"), data=form_data
        )
        task = Project.objects.get(name=name)

        self.assertEqual(task.name, name)
        self.assertEqual(task.is_completed, is_completed)

    def test_worker_create_form(self):
        username = "test_user"
        password = "asdf-6789"
        first_name = "test first"
        last_name = "test last"
        form_data = {
            "username": username,
            "password1": password,
            "password2": password,
            "first_name": first_name,
            "last_name": last_name,
            "position": 1,
            "is_active": True,
        }
        self.client.post(reverse("task_manager:worker-create"), data=form_data)
        user = get_user_model().objects.get(username=username)

        self.assertEqual(user.first_name, first_name)
        self.assertEqual(user.last_name, last_name)
        self.assertEqual(user.is_active, True)
