from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from teams.models import Team, TeamMember
from projects.models import Project
from accounts.models import User

@login_required
def team_list(request):
    if request.user.role == 'super_admin':
        teams = Team.objects.all()
    elif request.user.role == 'project_manager':
        teams = Team.objects.filter(manager=request.user)
    else:
        teams = Team.objects.filter(members=request.user)

    return render(request, 'teams/team_list.html', {'teams': teams})


@login_required
def team_create(request):
    if request.user.role not in ['super_admin', 'project_manager']:
        messages.error(request, 'You do not have permission!')
        return redirect('team_list')

    if request.method == 'POST':
        team_name = request.POST['team_name']
        project_id = request.POST['project']
        manager_id = request.POST['manager']
        members = request.POST.getlist('members')
        roles = request.POST.getlist('roles')

        team = Team.objects.create(
            team_name=team_name,
            project_id=project_id,
            manager_id=manager_id
        )

        for i, member_id in enumerate(members):
            role = roles[i] if i < len(roles) else 'developer'
            TeamMember.objects.create(
                team=team,
                user_id=member_id,
                role=role
            )

        messages.success(request, 'Team created successfully!')
        return redirect('team_list')

    projects = Project.objects.all()
    users = User.objects.all()
    return render(request, 'teams/team_form.html', {
        'projects': projects,
        'users': users,
        'action': 'Create'
    })


@login_required
def team_detail(request, pk):
    team = get_object_or_404(Team, pk=pk)
    members = TeamMember.objects.filter(team=team)
    return render(request, 'teams/team_detail.html', {
        'team': team,
        'members': members
    })


@login_required
def team_edit(request, pk):
    team = get_object_or_404(Team, pk=pk)

    if request.user.role not in ['super_admin', 'project_manager']:
        messages.error(request, 'You do not have permission!')
        return redirect('team_list')

    if request.method == 'POST':
        team.team_name = request.POST['team_name']
        team.project_id = request.POST['project']
        team.manager_id = request.POST['manager']
        team.save()

        TeamMember.objects.filter(team=team).delete()
        members = request.POST.getlist('members')
        roles = request.POST.getlist('roles')

        for i, member_id in enumerate(members):
            role = roles[i] if i < len(roles) else 'developer'
            TeamMember.objects.create(
                team=team,
                user_id=member_id,
                role=role
            )

        messages.success(request, 'Team updated successfully!')
        return redirect('team_list')

    projects = Project.objects.all()
    users = User.objects.all()
    current_members = TeamMember.objects.filter(team=team)
    return render(request, 'teams/team_form.html', {
        'team': team,
        'projects': projects,
        'users': users,
        'current_members': current_members,
        'action': 'Edit'
    })


@login_required
def team_delete(request, pk):
    team = get_object_or_404(Team, pk=pk)

    if request.user.role not in ['super_admin', 'project_manager']:
        messages.error(request, 'You do not have permission!')
        return redirect('team_list')

    if request.method == 'POST':
        team.delete()
        messages.success(request, 'Team deleted!')
        return redirect('team_list')

    return render(request, 'teams/team_confirm_delete.html', {'team': team})