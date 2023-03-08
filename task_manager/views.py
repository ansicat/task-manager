from django.contrib.auth import views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Subquery, OuterRef
from django.db.models.functions import Coalesce
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic

from task_manager.forms import TaskForm, ProjectForm, WorkerForm
from task_manager.models import Task, Project, Worker

SEGMENT_TASK = "task"
SEGMENT_PROJECT = "project"
SEGMENT_WORKER = "worker"


@login_required()
def index(request):
    """View function for the home page of the site."""

    active_tasks_count = Task.objects.filter(is_completed=False).count()
    completed_tasks_count = Task.objects.filter(is_completed=True).count()
    active_projects_count = Project.objects.filter(is_completed=False).count()
    completed_projects_count = Project.objects.filter(
        is_completed=True
    ).count()
    workers_count = Worker.objects.filter(
        is_superuser=0, is_active=True
    ).count()
    priority_tasks_list = (
        Task.objects.filter(is_completed=False)
        .order_by("priority")[:5]
        .select_related("project")
    )
    deadline_tasks_list = (
        Task.objects.filter(is_completed=False, deadline__isnull=False)
        .order_by("deadline")[:5]
        .select_related("project")
    )

    context = {
        "segment": "index",
        "active_tasks_count": active_tasks_count,
        "completed_tasks_count": completed_tasks_count,
        "active_projects_count": active_projects_count,
        "completed_projects_count": completed_projects_count,
        "workers_count": workers_count,
        "priority_tasks_list": priority_tasks_list,
        "deadline_tasks_list": deadline_tasks_list,
    }

    template = "task_manager/index.html"
    return render(request, template, context=context)


class LoginView(views.LoginView):
    redirect_authenticated_user = True
    success_url = "task_manager/index.html"


class SegmentTuneMixin(LoginRequiredMixin):
    """
    Mixin for setting initial context data of selected segment.

    segment - ID for highlighting of selected segment in sidebar
    edit_mode - how to show detail data of selected segment (view/edit mode)
    """

    def segment_context(self, segment, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = segment
        context["edit_mode"] = issubclass(
            self.__class__, generic.CreateView | generic.UpdateView
        )
        return context


class TaskListView(SegmentTuneMixin, generic.ListView):
    model = Task
    template_name = "task_manager/task_list.html"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        return self.segment_context(SEGMENT_TASK, **kwargs)

    def get_queryset(self):
        def to_bool(value, default=None):
            valid_values = {"true": True, "false": False}
            value = str(value).lower()

            if value in valid_values:
                return valid_values[value]

            return default

        search = self.request.GET.get("search")
        project = self.request.GET.get("project")
        worker = self.request.GET.get("worker")
        is_completed = to_bool(self.request.GET.get("completed"))

        queryset = (
            Task.objects.all()
            .select_related("project")
            .order_by("is_completed")
        )

        if is_completed is not None:
            queryset = queryset.filter(is_completed=is_completed)

        if search:
            queryset = queryset.filter(name__icontains=search)

        if project and str(project).isdigit():
            queryset = queryset.filter(project_id=project)

        if worker and str(worker).isdigit():
            queryset = queryset.filter(assignees__id=worker)

        return queryset


class TaskDetailView(SegmentTuneMixin, generic.DetailView):
    model = Task
    template_name = "task_manager/edit_form.html"

    def get_context_data(self, **kwargs):
        context = self.segment_context(SEGMENT_TASK, **kwargs)
        context["form"] = TaskForm(instance=self.object)
        return context


class TaskCreateView(SegmentTuneMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    template_name = "task_manager/edit_form.html"
    success_url = reverse_lazy("task_manager:task-list")

    def get_context_data(self, **kwargs):
        return self.segment_context(SEGMENT_TASK, **kwargs)


class TaskUpdateView(SegmentTuneMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "task_manager/edit_form.html"

    def get_context_data(self, **kwargs):
        return self.segment_context(SEGMENT_TASK, **kwargs)

    def get_success_url(self):
        return reverse_lazy(
            "task_manager:task-detail", kwargs={"pk": self.object.pk}
        )


def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return redirect("task_manager:task-list")


class ProjectListView(SegmentTuneMixin, generic.ListView):
    model = Project
    template_name = "task_manager/project_list.html"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        return self.segment_context(SEGMENT_PROJECT, **kwargs)

    def get_queryset(self):
        queryset = (
            Project.objects.all()
            .annotate(
                active_tasks=Coalesce(
                    Subquery(
                        Task.objects.filter(
                            is_completed=False, project__id=OuterRef("id")
                        )
                        .values("project__id")
                        .annotate(cnt=Coalesce(Count("project__id"), 0))
                        .values("cnt")
                    ),
                    0,
                )
            )
            .annotate(
                completed_tasks=Coalesce(
                    Subquery(
                        Task.objects.filter(
                            is_completed=True, project__id=OuterRef("id")
                        )
                        .values("project__id")
                        .annotate(cnt=Count("project__id"))
                        .values("cnt")
                    ),
                    0,
                )
            )
        )
        return queryset


class ProjectDetailView(SegmentTuneMixin, generic.DetailView):
    model = Project
    template_name = "task_manager/edit_form.html"

    def get_context_data(self, **kwargs):
        context = self.segment_context(SEGMENT_PROJECT, **kwargs)
        context["form"] = ProjectForm(instance=self.object)
        return context


class ProjectCreateView(SegmentTuneMixin, generic.CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "task_manager/edit_form.html"
    success_url = reverse_lazy("task_manager:project-list")

    def get_context_data(self, **kwargs):
        return self.segment_context(SEGMENT_PROJECT, **kwargs)


class ProjectUpdateView(SegmentTuneMixin, generic.UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "task_manager/edit_form.html"

    def get_context_data(self, **kwargs):
        return self.segment_context(SEGMENT_PROJECT, **kwargs)

    def get_success_url(self):
        return reverse_lazy(
            "task_manager:project-detail", kwargs={"pk": self.object.pk}
        )


def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project.delete()
    return redirect("task_manager:project-list")


class WorkerListView(SegmentTuneMixin, generic.ListView):
    model = Worker
    template_name = "task_manager/worker_list.html"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        return self.segment_context(SEGMENT_WORKER, **kwargs)

    def get_queryset(self):
        queryset = (
            Worker.objects.filter(is_superuser=0)
            .annotate(
                active_tasks=Coalesce(
                    Subquery(
                        Task.objects.filter(
                            is_completed=False, assignees__id=OuterRef("id")
                        )
                        .values("assignees__id")
                        .annotate(cnt=Count("assignees__id"))
                        .values("cnt")
                    ),
                    0,
                )
            )
            .annotate(
                completed_tasks=Coalesce(
                    Subquery(
                        Task.objects.filter(
                            is_completed=True, assignees__id=OuterRef("id")
                        )
                        .values("assignees__id")
                        .annotate(cnt=Count("assignees__id"))
                        .values("cnt")
                    ),
                    0,
                )
            )
            .select_related("position")
        )
        return queryset


class WorkerDetailView(SegmentTuneMixin, generic.DetailView):
    model = Worker
    template_name = "task_manager/edit_form.html"
    queryset = Worker.objects.all().select_related("position")

    def get_context_data(self, **kwargs):
        context = self.segment_context(SEGMENT_WORKER, **kwargs)
        context["form"] = WorkerForm(instance=self.object)
        return context


class WorkerCreateView(SegmentTuneMixin, generic.CreateView):
    model = Worker
    form_class = WorkerForm
    template_name = "task_manager/edit_form.html"
    success_url = reverse_lazy("task_manager:worker-list")

    def get_context_data(self, **kwargs):
        return self.segment_context(SEGMENT_WORKER, **kwargs)


class WorkerUpdateView(SegmentTuneMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerForm
    template_name = "task_manager/edit_form.html"
    queryset = Worker.objects.all().select_related("position")

    def get_context_data(self, **kwargs):
        return self.segment_context(SEGMENT_WORKER, **kwargs)

    def get_success_url(self):
        return reverse_lazy(
            "task_manager:worker-detail", kwargs={"pk": self.object.pk}
        )


@login_required
def worker_delete(request, pk):
    worker = get_object_or_404(Worker, pk=pk)
    worker.delete()
    return redirect("task_manager:worker-list")
