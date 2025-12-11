from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


    

class Project(models.Model):
    title = models.CharField(max_length=100)
    participants = models.ManyToManyField(
        User, 
        related_name='participant_projects',  # ← ОБЯЗАТЕЛЬНО!
        blank=True
    )
    admins = models.ManyToManyField(
        User,
        related_name='admin_projects',        # ← ОБЯЗАТЕЛЬНО!
        blank=True
    )
    
    def __str__(self):
        return self.title

class Kanban(models.Model):
    title = models.CharField(max_length=100)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='kanbans'  # ← Добавьте
    )
    
    def __str__(self):
        return f'{self.title} ({self.project.title})'

class Task(models.Model):
    title = models.CharField(max_length=200)
    performers = models.ManyToManyField(
        User, 
        related_name='performer_tasks',  # ← ОБЯЗАТЕЛЬНО!
        blank=True
    )
    deadline = models.DateTimeField(null=True, blank=True)
    kanban = models.ForeignKey(
        Kanban, 
        on_delete=models.CASCADE, 
        related_name='tasks',    # ← Добавьте
        null=True, 
        blank=True
    )
    created_at = models.DateTimeField(default=now)
    
    def __str__(self):
        return self.title
