from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
import jwt
from datetime import datetime, timedelta
from django.conf import settings 
from django.contrib.auth.models import (
	AbstractBaseUser, BaseUserManager, PermissionsMixin
)


# создал менеджер пользователей
# не знаю, мог ли бы я обойтись без него
# но пусть будет
# вообще я делаю регистрацию по jwt токенам по туториалу. пу-пу-пу надеюсь, что всё ок
class UserManager(BaseUserManager):
    use_in_migrations = True
    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('Users must have a username.')
        if email is None:
            raise TypeError('Users must have an email address.')
        
        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, username, email, password):
        if password is None:
            raise TypeError('Superusers must have a password.')
        
        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    username = models.CharField(max_length=255, unique=True, db_index=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    objects = UserManager()
    
    def __str__(self):
        return self.email
    
    @property
    def token(self):
        return self._generate_jwt_token()
    
    def get_full_name(self):
        return self.username    
    def get_short_name(self):
        return self.username
    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=60)
        
        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.timestamp())
        }, settings.SECRET_KEY, algorithm='HS256')
        
        return token


        

    

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
