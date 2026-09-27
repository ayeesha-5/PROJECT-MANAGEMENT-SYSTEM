from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from tasks.models import Task
from projects.models import Project
from accounts.models import User
from notifications.utils import notify_task_assigned, notify_task_completed
@login_required
def task_list(request):
    if request.user.role == 'super_admin':
        tasks = Task.objects.all()
    elif request.user.role == 'project_manager':
        tasks = Task.objects.filter(created_by=request.user)
    else:
        tasks = Task.objects.filter(assigned_to=request.user)

    return render(request, 'tasks/task_list.html', {'tasks': tasks})


@login_required
def task_create(request):
    if request.user.role not in ['super_admin', 'project_manager']:
        messages.error(request, 'You do not have permission to create tasks!')
        return redirect('task_list')

    if request.method == 'POST':
        task_name = request.POST['task_name']
        description = request.POST['description']
        project_id = request.POST['project']
        assigned_to_id = request.POST['assigned_to']
        priority = request.POST['priority']
        status = request.POST['status']
        deadline = request.POST['deadline']

        task = Task.objects.create(
            task_name=task_name,
            description=description,
            project_id=project_id,
            assigned_to_id=assigned_to_id,
            priority=priority,
            status=status,
            deadline=deadline,
            created_by=request.user
        )
        notify_task_assigned(task)
        messages.success(request, 'Task created successfully!')
        return redirect('task_list')

    projects = Project.objects.all()
    users = User.objects.all()
    return render(request, 'tasks/task_form.html', {
        'projects': projects,
        'users': users,
        'action': 'Create'
    })


@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'tasks/task_detail.html', {'task': task})


@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.user.role not in ['super_admin', 'project_manager']:
        messages.error(request, 'You do not have permission!')
        return redirect('task_list')

    if request.method == 'POST':
        task.task_name = request.POST['task_name']
        task.description = request.POST['description']
        task.project_id = request.POST['project']
        task.assigned_to_id = request.POST['assigned_to']
        task.priority = request.POST['priority']
        task.status = request.POST['status']
        task.deadline = request.POST['deadline']
        task.save()
        messages.success(request, 'Task updated successfully!')
        return redirect('task_list')

    projects = Project.objects.all()
    users = User.objects.all()
    return render(request, 'tasks/task_form.html', {
        'task': task,
        'projects': projects,
        'users': users,
        'action': 'Edit'
    })


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.user.role not in ['super_admin', 'project_manager']:
        messages.error(request, 'You do not have permission!')
        return redirect('task_list')

    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted!')
        return redirect('task_list')

    return render(request, 'tasks/task_confirm_delete.html', {'task': task})


@login_required
def task_update_status(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == 'POST':
        task.status = request.POST['status']
        task.save()
        if task.status == 'completed':
            notify_task_completed(task)
        messages.success(request, 'Task status updated!')
        return redirect('task_list')

    return render(request, 'tasks/task_update_status.html', {'task': task})