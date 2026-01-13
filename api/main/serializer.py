from rest_framework import serializers  
from .models import Kanban, Project, Task, OurUser
from django.contrib.auth import authenticate

from rest_framework.authtoken.models import Token

# TODO: Написать сериализаторы логина и регистрации

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        username = attrs.get('username')       
        password = attrs.get('password')
        if username and password:
            user = authenticate(
                username=username,
                password=password
            )
            if user:
                attrs['user'] = user
                return attrs
        raise serializers.ValidationError({
            "я хз"
        })

class RegisterSerializer(serializers.Serializer):
    username= serializers.CharField()
    email= serializers.EmailField()
    password = serializers.CharField(write_only=True, required=True)
    confirm_pass = serializers.CharField(write_only=True, required=True)
    
    def validate(self, attrs):
        if len(attrs['password'])<1:
            raise serializers.ValidationError({
                "username":"ВЗЛОМ ЖОПЫ"
            })
        if attrs['password'] != attrs['confirm_pass']:
            raise serializers.ValidationError(
                {
                    'password': 'Passwords do    not match'
                }
            )
        if OurUser.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError({
                "username":"Пользователь с таким username уже существует"
            })
        if OurUser.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({
                "username":"Пользователь с таким email уже существует"
            })
        return attrs
        
    def create(self, validated_data):
    # Обработайте confirm_pass, если есть
        validated_data.pop('confirm_pass', None)
        password = validated_data.pop('password')
    
    # Создаём объект OurUser
        user = OurUser.objects.create_user(
        username=validated_data['username'],
        email=validated_data['email'],
        password=password
    )
        return user  # Возвращаем ОБЪЕКТ, не словарь!

        
        
    
    
class ProjectSerializer(serializers.ModelSerializer):
    participants_ids = serializers.PrimaryKeyRelatedField(
        queryset=OurUser.objects.all(),
        source='participants',
        many=True,
        write_only=True,
        required=False
    )
    admins_ids = serializers.PrimaryKeyRelatedField(
        queryset=OurUser.objects.all(),
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
        queryset=OurUser.objects.all(),
        source='performers',
        many=True,
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'kanban_id', 'performers_ids', 'deadline']
