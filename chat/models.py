from django.db import models
from accounts.models import User
from projects.models import Project

class ChatRoom(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='chat_room')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat - {self.project.name}"


class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.content[:50]}"

    class Meta:
        ordering = ['timestamp']