from rest_framework import serializers
from .models import Kanban, Project, Task, User
from django.contrib.auth import authenticate

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length = 128,
        min_length = 8,
        write_only = True
    )
    token = serializers.CharField(max_length=128, read_only=True)

    class Meta:     
        model = User
        fields = ['email', 'username', 'password', 'token']
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    username = serializers.CharField(max_length=255, read_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    
    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)
        
        if email is None:
            raise serializers.ValidationError('An email address is required to log in.')
        
        if password is None:
            raise serializers.ValidationError('A password is required to log in.')
        
        user = authenticate(username=email, password=password)
        
        if user is None:
            raise serializers.ValidationError('A user with this email and password was not found.')
        
        if not user.is_active:
            raise serializers.ValidationError(
                "user with this email doesn't active"
            ) 
        return{
            "email":user.email,
            "username":user.username,
            "token":user.token
        }
    
    
class ProjectSerializer(serializers.ModelSerializer):
    participants_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='participants',
        many=True,
        write_only=True,
        required=False
    )
    admins_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='admins',
        many=True,
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Project
        fields = ['id', 'title', 'participants_ids', 'admins_ids']

    def create(self, validated_data):
        participants_data = validated_data.pop('participants_ids', [])
        admins_data = validated_data.pop('admins_ids', [])
        
        project = super().create(validated_data)
        project.participants.set(participants_data)
        project.admins.set(admins_data)
        return project

class KanbanSerializer(serializers.ModelSerializer):
    project_id = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(),
        source='project',
        write_only=True
    )
    
    class Meta:
        model = Kanban
        fields = ['id', 'title', 'project_id', 'project']

class TaskSerializer(serializers.ModelSerializer):
    kanban_id = serializers.PrimaryKeyRelatedField(
        queryset=Kanban.objects.all(),
        source='kanban',
        write_only=True
    )
    performers_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='performers',
        many=True,
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'kanban_id', 'performers_ids', 'deadline']
