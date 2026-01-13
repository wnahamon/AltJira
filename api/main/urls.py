from django.urls import path
from .views import *

urlpatterns = [
    path('projects/', ProjectMany.as_view()),
    path('projects/<int:id>/', ProjectOne.as_view()),
    path('kanbans/', KanbanMany.as_view()),
    path('kanbans/<int:id>/', KanbanOne.as_view()),
    path('tasks/', TaskMany.as_view()),
    path('tasks/<int:id>/', TaskOne.as_view()),
    path('reg/', RegistrationAPI.as_view()),
    path('login/', LoginAPI.as_view()),
]
