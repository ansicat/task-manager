from django.test import TestCase

from django.urls import reverse

from task_manager.models import Worker, Position, Task, TaskType, Project


INDEX_URL = reverse("task_manager:index")
TASK_LIST_URL = reverse("task_manager:task-list")
TASK_DETAIL_URL = reverse("task_manager:task-detail", kwargs={"pk": 1})
TASK_CREATE_URL = reverse("task_manager:task-create")
TASK_UPDATE_URL = reverse("task_manager:task-update", kwargs={"pk": 1})
TASK_DELETE_URL = reverse("task_manager:task-delete", kwargs={"pk": 1})
PROJECT_LIST_URL = reverse("task_manager:project-list")
PROJECT_DETAIL_URL = reverse("task_manager:project-detail", kwargs={"pk": 1})
PROJECT_CREATE_URL = reverse("task_manager:project-create")
PROJECT_UPDATE_URL = reverse("task_manager:project-update", kwargs={"pk": 1})
PROJECT_DELETE_URL = reverse("task_manager:project-delete", kwargs={"pk": 1})
WORKER_LIST_URL = reverse("task_manager:worker-list")
WORKER_DETAIL_URL = reverse("task_manager:worker-detail", kwargs={"pk": 1})
WORKER_CREATE_URL = reverse("task_manager:worker-create")
WORKER_UPDATE_URL = reverse("task_manager:worker-update", kwargs={"pk": 1})
WORKER_DELETE_URL = reverse("task_manager:worker-delete", kwargs={"pk": 1})


class TestFuncsMixin:
    def login_as_valid_user(self):
        position = Position.objects.create(name="test position")
        self.user = Worker.objects.create_user(
            username="test2",
            password="1qazcde3",
            position=position,
        )
        self.client.force_login(self.user)

    def check_segment_and_urls(self, segment, urls):
        for url, tpl in urls.items():
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200, url)
            self.assertEqual(response.context["segment"], segment, url)
            self.assertTemplateUsed(response, tpl)

    def create_new_project(self):
        project_name = "Test project"
        project = Project.objects.create(name=project_name)
        return project

    def create_new_task(self):
        task_name = "Task name"
        description = "Test description"
        deadline = "2020-05-25"
        is_completed = False
        priority = Task.PRIORITY_CHOICES[2][0]
        task_type_name = "Test task type"
        # position_name = "Test position"
        # user_name = "test_test_2"
        # user_password = "Test4pasS"
        # first_name = "Test _first_name"
        # last_name = "Test _last_name"

        task_type = TaskType.objects.create(name=task_type_name)
        project = self.create_new_project()
        worker = self.user
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

        return task


class PublicAccessTests(TestCase):
    def test_login_required(self):
        urls = [
            INDEX_URL,
            TASK_LIST_URL,
            TASK_DETAIL_URL,
            TASK_CREATE_URL,
            TASK_UPDATE_URL,
            TASK_DELETE_URL,
            PROJECT_LIST_URL,
            PROJECT_DETAIL_URL,
            PROJECT_CREATE_URL,
            PROJECT_UPDATE_URL,
            PROJECT_DELETE_URL,
            WORKER_LIST_URL,
            WORKER_DETAIL_URL,
            WORKER_CREATE_URL,
            WORKER_UPDATE_URL,
            WORKER_DELETE_URL,
        ]

        for url in urls:
            response = self.client.get(url)
            self.assertNotEqual(response.status_code, 200)


class PrivateTaskTests(TestFuncsMixin, TestCase):
    def setUp(self):
        self.login_as_valid_user()

    def test_segment_and_urls(self):
        self.create_new_task()

        urls = {
            TASK_LIST_URL: "task_manager/task_list.html",
            TASK_DETAIL_URL: "task_manager/edit_form.html",
            TASK_CREATE_URL: "task_manager/edit_form.html",
            TASK_UPDATE_URL: "task_manager/edit_form.html",
        }

        self.check_segment_and_urls("task", urls)

    def test_context_variables(self):
        names = [
            "segment",
            "active_tasks_count",
            "completed_tasks_count",
            "active_projects_count",
            "completed_projects_count",
            "workers_count",
            "priority_tasks_list",
            "deadline_tasks_list",
        ]
        response = self.client.get(INDEX_URL)

        for name in names:
            self.assertTrue(name in response.context)

        self.assertEqual(response.context["segment"], "index")

    def test_search_by_params(self):
        self.create_new_task()

        response = self.client.get(TASK_LIST_URL + "?search=task na")
        queryset = response.context["object_list"]
        self.assertEqual(queryset.count(), 1)

        response = self.client.get(
            TASK_LIST_URL + "?search=task na&completed=true"
        )
        queryset = response.context["object_list"]
        self.assertEqual(queryset.count(), 0)

        response = self.client.get(TASK_LIST_URL + "?search=abc")
        queryset = response.context["object_list"]
        self.assertEqual(queryset.count(), 0)

        response = self.client.get(TASK_LIST_URL + "?project=1")
        queryset = response.context["object_list"]
        self.assertEqual(queryset.count(), 1)

        response = self.client.get(
            TASK_LIST_URL + "?project=1j&completed=true"
        )
        queryset = response.context["object_list"]
        self.assertEqual(queryset.count(), 0)

        response = self.client.get(TASK_LIST_URL + "?worker=1")
        queryset = response.context["object_list"]
        self.assertEqual(queryset.count(), 1)

        response = self.client.get(TASK_LIST_URL + "?worker=1&completed=true")
        queryset = response.context["object_list"]
        self.assertEqual(queryset.count(), 0)

        response = self.client.get(TASK_LIST_URL + "?worker=3")
        queryset = response.context["object_list"]
        self.assertEqual(queryset.count(), 0)

    def test_task_delete(self):
        self.create_new_task()

        count = Task.objects.filter(pk=1).count()
        self.assertEqual(count, 1)

        response = self.client.get(TASK_DELETE_URL)
        self.assertRedirects(response, TASK_LIST_URL)

        count = Task.objects.filter(pk=1).count()
        self.assertEqual(count, 0)


class PrivateProjectTests(TestFuncsMixin, TestCase):
    def setUp(self):
        self.login_as_valid_user()

    def test_segment_and_urls(self):
        self.create_new_project()

        urls = {
            PROJECT_LIST_URL: "task_manager/project_list.html",
            PROJECT_DETAIL_URL: "task_manager/edit_form.html",
            PROJECT_CREATE_URL: "task_manager/edit_form.html",
            PROJECT_UPDATE_URL: "task_manager/edit_form.html",
        }

        self.check_segment_and_urls("project", urls)

    def test_project_delete(self):
        self.create_new_project()

        count = Project.objects.filter(pk=1).count()
        self.assertEqual(count, 1)

        response = self.client.get(PROJECT_DELETE_URL)
        self.assertRedirects(response, PROJECT_LIST_URL)

        count = Project.objects.filter(pk=1).count()
        self.assertEqual(count, 0)


class PrivateWorkerTests(TestFuncsMixin, TestCase):
    def setUp(self):
        self.login_as_valid_user()

    def test_segment_and_urls(self):
        urls = {
            WORKER_LIST_URL: "task_manager/worker_list.html",
            WORKER_DETAIL_URL: "task_manager/edit_form.html",
            WORKER_CREATE_URL: "task_manager/edit_form.html",
            WORKER_UPDATE_URL: "task_manager/edit_form.html",
        }

        self.check_segment_and_urls("worker", urls)

    def test_worker_delete(self):
        user = Worker.objects.create_user(
            username="test_delete",
            password="1qazcde3",
            position_id=1,
        )

        count = Worker.objects.filter(pk=user.id).count()
        self.assertEqual(count, 1)

        response = self.client.get(
            reverse("task_manager:worker-delete", kwargs={"pk": user.id})
        )
        self.assertRedirects(response, WORKER_LIST_URL)

        count = Worker.objects.filter(pk=user.id).count()
        self.assertEqual(count, 0)
