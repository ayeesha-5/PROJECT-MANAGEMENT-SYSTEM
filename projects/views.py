from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from projects.models import Project
from accounts.models import User
from notifications.utils import notify_project_created, notify_new_members_added


@login_required
def project_list(request):
    if request.user.role == 'super_admin':
        projects = Project.objects.all()
    elif request.user.role == 'project_manager':
        projects = Project.objects.filter(created_by=request.user)
    else:
        projects = request.user.assigned_projects.all()

    return render(request, 'projects/project_list.html', {'projects': projects})


@login_required
def project_create(request):
    if request.user.role not in ['super_admin', 'project_manager']:
        messages.error(request, 'You do not have permission to create projects!')
        return redirect('project_list')

    if request.method == 'POST':
        name        = request.POST['name']
        description = request.POST['description']
        start_date  = request.POST['start_date']
        end_date    = request.POST['end_date']
        priority    = request.POST['priority']
        budget      = request.POST['budget']
        status      = request.POST['status']
        members     = request.POST.getlist('members')

        project = Project.objects.create(
            name=name,
            description=description,
            start_date=start_date,
            end_date=end_date,
            priority=priority,
            budget=budget,
            status=status,
            created_by=request.user
        )
        project.members.set(members)

        # ✅ FIX: notify all members that they were added to this project
        notify_project_created(project)

        messages.success(request, 'Project created successfully!')
        return redirect('project_list')

    users = User.objects.all()
    return render(request, 'projects/project_form.html', {'users': users, 'action': 'Create'})


@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'projects/project_detail.html', {'project': project})


@login_required
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.user.role not in ['super_admin', 'project_manager']:
        messages.error(request, 'You do not have permission!')
        return redirect('project_list')

    if request.method == 'POST':
        # ✅ FIX: capture OLD members before update to detect newly added ones
        old_member_ids = set(project.members.values_list('id', flat=True))

        project.name        = request.POST['name']
        project.description = request.POST['description']
        project.start_date  = request.POST['start_date']
        project.end_date    = request.POST['end_date']
        project.priority    = request.POST['priority']
        project.budget      = request.POST['budget']
        project.status      = request.POST['status']
        new_member_ids      = set(int(i) for i in request.POST.getlist('members'))
        project.members.set(new_member_ids)
        project.save()

        # ✅ FIX: notify only newly added members
        newly_added_ids = new_member_ids - old_member_ids
        if newly_added_ids:
            notify_new_members_added(project, newly_added_ids)

        messages.success(request, 'Project updated successfully!')
        return redirect('project_list')

    users = User.objects.all()
    return render(request, 'projects/project_form.html', {
        'project': project,
        'users': users,
        'action': 'Edit'
    })


@login_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.user.role not in ['super_admin', 'project_manager']:
        messages.error(request, 'You do not have permission!')
        return redirect('project_list')

    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project deleted!')
        return redirect('project_list')

    return render(request, 'projects/project_confirm_delete.html', {'project': project})
