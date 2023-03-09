from django.test import TestCase

from task_manager.models import Worker, Position, Project, TaskType, Task


class TaskTypeTests(TestCase):
    def test_create_task_type(self):
        task_type_name = "Test task type"

        task_type = TaskType.objects.create(name=task_type_name)

        self.assertEqual(task_type.name, task_type_name)
        self.assertEqual(str(task_type), task_type_name)


class PositionTests(TestCase):
    def test_create_position(self):
        position_name = "Test position"

        position = Position.objects.create(name=position_name)

        self.assertEqual(position.name, position_name)
        self.assertEqual(str(position), position_name)


class ProjectTests(TestCase):
    def test_create_project(self):
        project_name = "Test project"

        project = Project.objects.create(name=project_name)

        self.assertEqual(project.name, project_name)
        self.assertEqual(str(project), project_name)
        self.assertEqual(
            project.get_absolute_url(), f"/projects/{project.id}/"
        )


class WorkerTests(TestCase):
    def test_create_worker(self):
        user_name = "test_test"
        user_password = "Test4pasS"
        first_name = "Test first_name"
        last_name = "Test last_name"
        position_name = "Test developer"

        position = Position.objects.create(name=position_name)
        worker = Worker.objects.create_user(
            username=user_name,
            password=user_password,
            first_name=first_name,
            last_name=last_name,
            position=position,
        )

        self.assertEqual(worker.username, user_name)
        self.assertTrue(worker.check_password(user_password))
        self.assertEqual(worker.first_name, first_name)
        self.assertEqual(worker.last_name, last_name)
        self.assertEqual(worker.position.name, position_name)
        self.assertEqual(
            str(worker),
            f"{user_name} ({first_name} {last_name})",
        )
        self.assertEqual(worker.get_absolute_url(), f"/workers/{worker.id}/")


class TaskTests(TestCase):
    def test_create_task(self):
        task_name = "Task name"
        description = "Test description"
        deadline = "2020-05-25"
        is_completed = False
        priority = Task.PRIORITY_CHOICES[2][0]
        task_type_name = "Test task type"
        position_name = "Test position"
        project_name = "Test project"
        user_name = "test_test_2"
        user_password = "Test4pasS"
        first_name = "Test first_name"
        last_name = "Test last_name"

        task_type = TaskType.objects.create(name=task_type_name)
        position = Position.objects.create(name=position_name)
        project = Project.objects.create(name=project_name)
        worker = Worker.objects.create_user(
            username=user_name,
            password=user_password,
            first_name=first_name,
            last_name=last_name,
            position=position,
        )
        task = Task.objects.create(
            name=task_name,
            description=description,
            deadline=deadline,
            is_completed=is_completed,
            priority=priority,
            task_type=task_type,
            project=project,
        )
        task.assignees.set([worker])

        self.assertEqual(task.name, task_name)
        self.assertEqual(str(task), task_name)
        self.assertEqual(task.get_absolute_url(), f"/tasks/{task.id}/")
        self.assertEqual(task.assignees.count(), 1)
        self.assertEqual(
            task.assignees.values_list("username")[0], (worker.username,)
        )
