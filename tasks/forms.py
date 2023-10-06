from django.forms import ModelForm
from .models import Task

class createTaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description']