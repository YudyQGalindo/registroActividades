from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseForbidden
from .forms import createTaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.

# Mostrar la página principal
def home(request):
    return render(request, 'home.html')

# Registrar un nuevo usuario
def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        # Verifica si el usuario actual es Admin
        if request.user.username == 'Admin':
            if request.POST['password1'] == request.POST['password2']:
                # Registro de usuario
                try:
                    user = User.objects.create_user(
                        username=request.POST['username'], password=request.POST['password1'])
                    user.save()
                    login(request, user)
                    return redirect('tasks')
                except:
                    return render(request, 'signup.html', {
                        'form': UserCreationForm,
                        "error": 'Username already exists'
                    })
            return render(request, 'signup.html', {
                'form': UserCreationForm,
                "error": 'Password do not match'
            })
        else:
            # Si el usuario no es Admin, mostrar una página de acceso denegado
            return HttpResponseForbidden("Acceso denegado")

# Mostrar las actividades pendientes de un usuario
@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {'tasks': tasks})

# Mostrar las actividades completadas de un usuario
@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(
        user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks.html', {'tasks': tasks})

# Crear una nueva actividad
@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': createTaskForm
        })
    else:
        try:
            form = createTaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {
                'form': createTaskForm,
                'error': '¡Error: por favor ingrese datos válidos!'
            })

# Actualizar las actividades pendientes de un usuario
@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = createTaskForm(instance=task)
        return render(request, 'task_detail.html', {
            'task': task, 'form': form
        })
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = createTaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {
                'task': task, 'form': form,
                'error': "Error: al actualizar los datos, intente de nuevo."
            })

# Marcar una actividad como completada
@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

# Eliminar una actividad
@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

# Cerrar sesión
@login_required
def signout(request):
    logout(request)
    return redirect('home')

# Inicio de sesión
def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            if user.username == 'Admin':
                # El usuario es un administrador, redirigir a la vista de registro de usuarios
                login(request, user)
                return redirect('signup')
            else:
                # El usuario no es un administrador, redirigir a la vista de tareas pendientes
                login(request, user)
                return redirect('tasks')
        else:
            # Los datos ingresados están erróneos
            return render(request, 'signin.html', {
                'form': AuthenticationForm(),
                'error': '¡Error: Usuario o contraseña incorrectos!'
            })
