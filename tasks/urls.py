from django.urls import path
from tasks import views

urlpatterns = [
    path('tasks/', views.view_tasks, name='tasks'),
    path('tasks/new_task', views.new_task, name='new_task')
]
