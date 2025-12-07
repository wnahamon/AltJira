from django.urls import path
from .views import *

urlpatterns = [
    path('api/projects/', ProjectMany.as_view()),
    path('api/projects/<int:id>/', ProjectOne.as_view()),
    path('api/kanbans/', KanbanMany.as_view()),
    path('api/kanbans/<int:id>/', KanbanOne.as_view()),
    path('api/tasks/', TaskMany.as_view()),
    path('api/tasks/<int:id>/', TaskOne.as_view()),
]
