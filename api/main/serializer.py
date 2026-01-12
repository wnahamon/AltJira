from rest_framework import serializers  
from .models import Kanban, Project, Task, User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

# TODO: Написать сериализаторы логина и регистрации

class LoginSerializer(serializers.Serializer):
    
    class Meta:
        model = User
        fields = ['username', 'password']
    
    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user:
            return user
        else:
            raise serializers.ValidationError("Invalid credentials")
            
    
class RegisterSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        if validated_data['password'] == validated_data['password_confirm']:
            user = User.objects.create_user(
                username=validated_data['username'],
                password=validated_data['password']
            )
            return user
        
        
    
    
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
