from rest_framework import serializers
from .models import Kanban, Project, Task  # Canban → Kanban
from django.contrib.auth.models import User
class ProjectSerializer(serializers.ModelSerializer):
    # Убираем ManyToMany из write-only, показываем только ID в ответе
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
        fields = ['id', 'title', 'participants_ids', 'admins_ids', 'created_at']
        read_only_fields = ['created_at']

class KanbanSerializer(serializers.ModelSerializer):
    project_id = serializers.IntegerField(write_only=True, source='project.id')
    
    class Meta:
        model = Kanban  # Canban → Kanban
        fields = ['id', 'title', 'project_id', 'project', 'created_at', 'updated_at']
        read_only_fields = ['project', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        project_id = validated_data.pop('project_id')
        project = Project.objects.get(id=project_id)
        validated_data['project'] = project
        return super().create(validated_data)

class TaskSerializer(serializers.ModelSerializer):
    kanban_id = serializers.IntegerField(write_only=True, source='kanban.id')
    performers_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), 
        source='performers', 
        many=True, 
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'kanban_id', 'performers_ids', 
                 'deadline', 'created_at']
        read_only_fields = ['created_at']
    
    def create(self, validated_data):
        kanban_id = validated_data.pop('kanban_id')
        kanban = Kanban.objects.get(id=kanban_id)
        validated_data['kanban'] = kanban
        return super().create(validated_data)
