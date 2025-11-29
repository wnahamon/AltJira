from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework import status
from .serializer import ProjectSerializer, KanbanSerializer, TaskSerializer  # Добавь сериализаторы
from .models import Project, Kanban, Task

# 1. Список/создание проектов
class ProjectGetCreate(APIView):
    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):  # create → post
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 2. Один проект (GET/PATCH/DELETE)
class ProjectGetPatchDelete(APIView):
    def get(self, request, id):
        project = Project.objects.get(id=id)  # filter → get, objectsm → objects
        serializer = ProjectSerializer(project)  # many=False
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, id):
        project = Project.objects.get(id=id)
        serializer = ProjectSerializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        project = Project.objects.get(id=id)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)  # 400 → 204

# 3. Список/создание канбанов
class KanbanMany(APIView):
    def get(self, request):
        kanbans = Kanban.objects.all()  # Project → Kanban
        serializer = KanbanSerializer(kanbans, many=True)  # ProjectSerializer → KanbanSerializer
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):  # create → post
        serializer = KanbanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 4. Один канбан (GET/PATCH/DELETE)
class KanbanGetPatchDelete(APIView):
    def get(self, request, id):
        kanban = Kanban.objects.get(id=id)  # Project → Kanban, objectsm → objects
        serializer = KanbanSerializer(kanban)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, id):
        kanban = Kanban.objects.get(id=id)
        serializer = KanbanSerializer(kanban, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        kanban = Kanban.objects.get(id=id)
        kanban.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)  # 400 → 204
