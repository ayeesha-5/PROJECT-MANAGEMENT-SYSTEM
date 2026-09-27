from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from projects.models import Project
from tasks.models import Task
from accounts.models import User
from teams.models import Team

@login_required
def reports_view(request):
    # Project stats
    total_projects = Project.objects.count()
    completed_projects = Project.objects.filter(status='completed').count()
    inprogress_projects = Project.objects.filter(status='in_progress').count()
    pending_projects = Project.objects.filter(status='pending').count()
    onhold_projects = Project.objects.filter(status='on_hold').count()

    # Task stats
    total_tasks = Task.objects.count()
    completed_tasks = Task.objects.filter(status='completed').count()
    inprogress_tasks = Task.objects.filter(status='in_progress').count()
    pending_tasks = Task.objects.filter(status='pending').count()
    testing_tasks = Task.objects.filter(status='testing').count()

    # User stats
    total_users = User.objects.count()
    total_teams = Team.objects.count()

    # Per user performance
    employees = User.objects.filter(role='employee')
    employee_stats = []
    for emp in employees:
        assigned = Task.objects.filter(assigned_to=emp).count()
        completed = Task.objects.filter(assigned_to=emp, status='completed').count()
        score = int((completed / assigned) * 100) if assigned > 0 else 0
        employee_stats.append({
            'username': emp.username,
            'email': emp.email,
            'assigned': assigned,
            'completed': completed,
            'score': score
        })

    # Recent projects
    recent_projects = Project.objects.order_by('-created_at')[:5]

    # Recent tasks
    recent_tasks = Task.objects.order_by('-created_at')[:5]

    context = {
        'total_projects': total_projects,
        'completed_projects': completed_projects,
        'inprogress_projects': inprogress_projects,
        'pending_projects': pending_projects,
        'onhold_projects': onhold_projects,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'inprogress_tasks': inprogress_tasks,
        'pending_tasks': pending_tasks,
        'testing_tasks': testing_tasks,
        'total_users': total_users,
        'total_teams': total_teams,
        'employee_stats': employee_stats,
        'recent_projects': recent_projects,
        'recent_tasks': recent_tasks,
    }
    return render(request, 'reports/reports.html', context)