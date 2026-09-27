from notifications.models import Notification
from accounts.models import User


def send_notification(user, title, message, notification_type='general'):
    Notification.objects.create(
        user=user,
        title=title,
        message=message,
        notification_type=notification_type
    )


# ── Project Notifications ─────────────────────────────────────────────────────

def notify_project_created(project):
    """Notify ALL members when a new project is created and they are added."""
    for member in project.members.all():
        send_notification(
            user=member,
            title='Added to Project 📁',
            message=f'You have been added to project: "{project.name}". Start date: {project.start_date}.',
            notification_type='project_created'
        )


def notify_new_members_added(project, new_member_ids):
    """Notify only NEWLY added members when a project is edited."""
    members = User.objects.filter(id__in=new_member_ids)
    for member in members:
        send_notification(
            user=member,
            title='Added to Project 📁',
            message=f'You have been added to project: "{project.name}".',
            notification_type='project_created'
        )


# ── Task Notifications ────────────────────────────────────────────────────────

def notify_task_assigned(task):
    """Notify the employee when a task is assigned to them."""
    if task.assigned_to:
        send_notification(
            user=task.assigned_to,
            title='New Task Assigned ✅',
            message=f'You have been assigned: "{task.task_name}" in project "{task.project.name}". Deadline: {task.deadline}.',
            notification_type='task_assigned'
        )


def notify_task_completed(task):
    """Notify the task creator (manager) when a task is marked completed."""
    # ✅ FIX: guard against missing created_by
    if task.created_by:
        send_notification(
            user=task.created_by,
            title='Task Completed 🎉',
            message=f'Task "{task.task_name}" in project "{task.project.name}" has been marked as completed!',
            notification_type='task_completed'
        )


# ── File Notifications ────────────────────────────────────────────────────────

def notify_file_uploaded(project_file):
    """Notify all project members (except uploader) when a file is uploaded."""
    for member in project_file.project.members.all():
        if member != project_file.uploaded_by:
            send_notification(
                user=member,
                title='New File Uploaded 📎',
                message=f'{project_file.uploaded_by.username} uploaded "{project_file.title}" in project "{project_file.project.name}".',
                notification_type='file_uploaded'
            )
