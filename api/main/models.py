from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.timezone import now
from django.conf import settings


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)


class OurUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


class Project(models.Model):
    title = models.CharField(max_length=100)
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='participant_projects',
        blank=True,
    )
    admins = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='admin_projects',
        blank=True,
    )

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
    title = models.CharField(max_length=200)
    performers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='performer_tasks',
        blank=True,
    )
    deadline = models.DateTimeField(null=True, blank=True)
    kanban = models.ForeignKey(
        Kanban,
        on_delete=models.CASCADE,
        related_name='tasks',
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.title
