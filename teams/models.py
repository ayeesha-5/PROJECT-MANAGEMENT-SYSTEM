from django.db import models
from accounts.models import User
from projects.models import Project

class Team(models.Model):
    ROLE_CHOICES = (
        ('manager', 'Manager'),
        ('developer', 'Developer'),
        ('tester', 'Tester'),
        ('designer', 'Designer'),
    )

    team_name = models.CharField(max_length=200)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='teams')
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='managed_teams')
    members = models.ManyToManyField(User, through='TeamMember', related_name='teams')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.team_name


class TeamMember(models.Model):
    ROLE_CHOICES = (
        ('manager', 'Manager'),
        ('developer', 'Developer'),
        ('tester', 'Tester'),
        ('designer', 'Designer'),
    )
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='developer')

    def __str__(self):
        return f"{self.user.username} - {self.team.team_name} ({self.role})"