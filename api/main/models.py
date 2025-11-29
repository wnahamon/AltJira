from django.db import models
""" TODO
1. Пересмотри модели чтобы были правильные 
"""
class Project(models.Model):
    title = models.CharField(max_length=100)
    participants = models.ManyToManyField
    admins = models.ManyToManyField

class Canban(models.Model):
    title = models.CharField(max_length=100)
    models.ForeignKey("app.Model", on_delete=models.CASCADE)

class Task(models.Model):
    title = models.CharField(max_length=100)
    performers = models.CharField(max_length=100)
    deadline = models.CharField(max_length=100)