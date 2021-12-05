from django.urls import path
from tasks import views

urlpatterns = [
    path('tasks/', views.view_tasks, name='tasks'),
]
