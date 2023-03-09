from django import forms
from django.contrib.auth.forms import UserCreationForm

from task_manager.models import Task, Project, Worker


class ControlStyleMixin:
    """Configure styles of controls for view/edit mode."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for item in self.visible_fields():
            if isinstance(item.field, forms.BooleanField):
                item.field.widget.attrs["class"] = "form-check-input"
            else:
                item.field.widget.attrs["class"] = "form-control"


class TaskForm(ControlStyleMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Restrict the queryset for the "assignees" form field
        queryset = Worker.objects.filter(is_superuser=0)
        self.fields["assignees"].queryset = queryset

    class Meta:
        model = Task
        fields = "__all__"
        widgets = {
            "description": forms.Textarea(),
        }


class ProjectForm(ControlStyleMixin, forms.ModelForm):
    class Meta:
        model = Project
        fields = "__all__"


class WorkerForm(ControlStyleMixin, UserCreationForm):
    class Meta:
        model = Worker
        fields = [
            "username",
            "password1",
            "password2",
            "first_name",
            "last_name",
            "position",
            "is_active",
        ]
