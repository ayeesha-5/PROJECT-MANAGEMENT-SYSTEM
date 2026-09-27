from django.db import models
from accounts.models import User

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('task_assigned', 'Task Assigned'),
        ('task_completed', 'Task Completed'),
        ('deadline_reminder', 'Deadline Reminder'),
        ('file_uploaded', 'File Uploaded'),
        ('team_message', 'New Team Message'),
        ('project_created', 'Project Created'),
        ('general', 'General'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=30, choices=NOTIFICATION_TYPES, default='general')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"

    class Meta:
        ordering = ['-created_at']