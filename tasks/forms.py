from django import forms
from django.forms import ModelForm
from .models import Task
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

class createTaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description']

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']

class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']
        widget = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'})
        }