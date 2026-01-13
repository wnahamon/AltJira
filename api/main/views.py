from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from .serializer import (
    ProjectSerializer, KanbanSerializer,
    TaskSerializer, RegisterSerializer,
    LoginSerializer
    )
from .models import Project, Kanban, Task, OurUser

# TODO: Написать регистрацию и логин 
# 😢
class RegistrationAPI(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # Создаёт и возвращает User-объект
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                },
                "token": token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class LoginAPI(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = OurUser(
                username=serializer.data['username'],
                email=serializer.data['email'], 
                password=serializer.data['password']
            )
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "user":user,
                "token":token
            })
        return Response({
            "erroe":serializer.errors
        })




class ProjectMany(APIView):
    def get(self, request):
        projects = Project.objects.filter(participants=request.user)
        serializer = ProjectSerializer(projects, many=True)
        return Response(
            serializer.data, 
            status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, 
                status=status.HTTP_201_CREATED)
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST)





class ProjectOne(APIView):
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
class KanbanOne(APIView):
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

class TaskMany(APIView):
    def get(self, request):
        tasks  = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=200)
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskOne(APIView):
    def get(self, request, id):
        tasks = Task.objects.get(id=id) 
        serializer = TaskSerializer(tasks)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, id):
        tasks = Task.objects.get(id=id)
        serializer = KanbanSerializer(tasks, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        tasks = Task.objects.get(id=id)
        tasks.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)