from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response 
from .serializer import ProjectSerializer
from .models import Project
""" ::TODO::
1. сделать 4 вьюхи
"""

class ProjectAPIview(APIView):
    
    def get(self, request):
        projects = Project.objectsm.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=200)
    
    def create(self,request):
        item = Project(
            
        )
        pass
    