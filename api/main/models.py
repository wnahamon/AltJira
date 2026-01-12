from django.db import models
from django.contrib.auth.models import User, AbstractUser, BaseUserManager
from django.utils.timezone import now
from datetime import datetime, timedelta
from django.conf import settings 


    
class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        
        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(username, email, password)
        user.is_admin = True
        user.save()
        return user
    
    
class OurUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)
    objects=UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = 'email'
    def __str__(self):
        return self.username
            
        
    

class Project(models.Model):
    title = models.CharField(max_length=100)
    participants = models.ManyToManyField(
        User, 
        related_name='participant_projects', 
        blank=True
    )
    admins = models.ManyToManyField(
        User,
        related_name='admin_projects',       
        blank=True
    )
    
    def __str__(self):
        return self.title
    
    
    

class Kanban(models.Model):
    title = models.CharField(max_length=100)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='kanbans'
    )
    
    def __str__(self):
        return f'{self.title} ({self.project.title})'

class Task(models.Model):
    title = models.CharField(max_length=200)
    performers = models.ManyToManyField(
        User, 
        related_name='performer_tasks',
        blank=True
    )
    deadline = models.DateTimeField(null=True, blank=True)
    kanban = models.ForeignKey(
        Kanban, 
        on_delete=models.CASCADE, 
        related_name='tasks',    
        null=True, 
        blank=True
    )
    created_at = models.DateTimeField(default=now)
    
    def __str__(self):
        return self.title
