from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import User
from projects.models import Project
from tasks.models import Task
from notifications.models import Notification
 

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST['role']

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists!')
            return redirect('register')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role
        )
        messages.success(request, 'Registration successful! Please login.')
        return redirect('login')

    return render(request, 'accounts/register.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
            if user:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid password!')
        except User.DoesNotExist:
            messages.error(request, 'Email not found!')

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    messages.info(request, 'Logged out successfully!')
    return redirect('login')


# Replace your existing dashboard_view in accounts/views.py with this:


@login_required
def dashboard_view(request):
    user = request.user

    # Project stats
    if user.role == 'super_admin':
        total_projects    = Project.objects.count()
        active_projects   = Project.objects.filter(status='in_progress').count()
        completed_projects = Project.objects.filter(status='completed').count()
        pending_projects  = Project.objects.filter(status='pending').count()
        total_tasks       = Task.objects.count()
        completed_tasks   = Task.objects.filter(status='completed').count()
        pending_tasks     = Task.objects.filter(status='pending').count()
        recent_projects   = Project.objects.order_by('-created_at')[:5]
        recent_tasks      = Task.objects.order_by('-created_at')[:5]
    elif user.role == 'project_manager':
        total_projects    = Project.objects.filter(created_by=user).count()
        active_projects   = Project.objects.filter(created_by=user, status='in_progress').count()
        completed_projects = Project.objects.filter(created_by=user, status='completed').count()
        pending_projects  = Project.objects.filter(created_by=user, status='pending').count()
        total_tasks       = Task.objects.filter(created_by=user).count()
        completed_tasks   = Task.objects.filter(created_by=user, status='completed').count()
        pending_tasks     = Task.objects.filter(created_by=user, status='pending').count()
        recent_projects   = Project.objects.filter(created_by=user).order_by('-created_at')[:5]
        recent_tasks      = Task.objects.filter(created_by=user).order_by('-created_at')[:5]
    else:
        total_projects    = user.assigned_projects.count()
        active_projects   = user.assigned_projects.filter(status='in_progress').count()
        completed_projects = user.assigned_projects.filter(status='completed').count()
        pending_projects  = user.assigned_projects.filter(status='pending').count()
        total_tasks       = Task.objects.filter(assigned_to=user).count()
        completed_tasks   = Task.objects.filter(assigned_to=user, status='completed').count()
        pending_tasks     = Task.objects.filter(assigned_to=user, status='pending').count()
        recent_projects   = user.assigned_projects.order_by('-created_at')[:5]
        recent_tasks      = Task.objects.filter(assigned_to=user).order_by('-created_at')[:5]

    unread_notifications = Notification.objects.filter(user=user, is_read=False).count()

    context = {
        'user': user,
        'total_projects': total_projects,
        'active_projects': active_projects,
        'completed_projects': completed_projects,
        'pending_projects': pending_projects,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'recent_projects': recent_projects,
        'recent_tasks': recent_tasks,
        'unread_notifications': unread_notifications,
    }
    return render(request, 'accounts/dashboard.html', context)

@login_required
def profile_view(request):
    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.phone = request.POST.get('phone', '')
        if 'profile_pic' in request.FILES:
            request.user.profile_pic = request.FILES['profile_pic']
        request.user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    return render(request, 'accounts/profile.html', {'user': request.user})


@login_required
def change_password_view(request):
    if request.method == 'POST':
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        if not request.user.check_password(old_password):
            messages.error(request, 'Old password is incorrect!')
            return redirect('change_password')

        if new_password != confirm_password:
            messages.error(request, 'New passwords do not match!')
            return redirect('change_password')

        request.user.set_password(new_password)
        request.user.save()
        update_session_auth_hash(request, request.user)
        messages.success(request, 'Password changed successfully!')
        return redirect('dashboard')

    return render(request, 'accounts/change_password.html')


def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return redirect('forgot_password')

        try:
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Password reset successful! Please login.')
            return redirect('login')
        except User.DoesNotExist:
            messages.error(request, 'No account found with this email!')

    return render(request, 'accounts/forgot_password.html')