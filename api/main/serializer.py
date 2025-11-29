from rest_framework import serializers
from .models import Canban, Project, Task

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"
        
class CanbanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Canban
        fields = "__all__"
        
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"