from django.db import models
from accounts.models import User
from projects.models import Project

class ProjectFile(models.Model):
    FILE_TYPE_CHOICES = (
        ('pdf', 'PDF'),
        ('document', 'Document'),
        ('image', 'Image'),
        ('zip', 'ZIP'),
        ('other', 'Other'),
    )

    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='project_files/')
    file_type = models.CharField(max_length=20, choices=FILE_TYPE_CHOICES, default='other')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='files')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_files')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_file_size(self):
        try:
            return f"{self.file.size / 1024:.1f} KB"
        except:
            return "Unknown"