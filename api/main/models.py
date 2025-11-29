from django.db import models
from django.contrib.auth.models import User
""" TODO
1. Пересмотри модели чтобы были правильные 
"""
class Project(models.Model):
    title = models.CharField(max_length=100)
    participants = models.ManyToManyField(User, related_name='projects_participant', blank=True)
    admins = models.ManyToManyField(User, related_name='projects_participant', blank=True)
    def __str__(self):
        return self.title

class Kanban(models.Model):
    title = models.CharField(max_length=100)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='kanbans',
    )

    def __str__(self):
        return f'{self.title} ({self.project.title})'

class Task(models.Model):
    title = models.CharField(max_length=100)
    performers = models.CharField(max_length=100)
    deadline = models.CharField(max_length=100)