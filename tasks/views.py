from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from .models import Task
from .forms import TaskForm, CustomUserCreationForm

def home(request):
    if request.user.is_authenticated:
        return redirect('task_list')
    return render(request, 'tasks/home.html')

@login_required
def task_list(request):
    tasks = Task.objects.filter(responsible=request.user)
    return render(request, 'tasks/task_list.html', {
        'tasks': tasks,
        'todo_count': tasks.filter(status='TODO').count(),
        'in_progress_count': tasks.filter(status='IN_PROGRESS').count(),
        'done_count': tasks.filter(status='DONE').count(),
    })

@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk, responsible=request.user)
    return render(request, 'tasks/task_detail.html', {'task': task})

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.responsible = request.user  # Always set the current user as responsible
            task.save()
            messages.success(request, 'Task created successfully!')
            return redirect('task_list')
    else:
        form = TaskForm()  # No need for initial since responsible is set in the view
    
    return render(request, 'tasks/task_form.html', {'form': form, 'title': 'Create Task'})




@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk, responsible=request.user)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            edited_task = form.save(commit=False)
            # Ensure the task remains assigned to the current user
            edited_task.responsible = request.user
            edited_task.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    
    return render(request, 'tasks/task_form.html', {'form': form, 'title': 'Edit Task'})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, responsible=request.user)
    
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully!')
        return redirect('task_list')
    
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})

def register(request):
    if request.user.is_authenticated:
        return redirect('task_list')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('task_list')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'tasks/register.html', {'form': form})



