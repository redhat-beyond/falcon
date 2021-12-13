from django.urls import path
from tasks import views

urlpatterns = [
    path('tasks/', views.view_tasks, name='tasks'),
    path('tasks/new_task', views.new_task, name='new_task'),
    path('tasks/<str:pk>', views.view_single_task, name="view_single_task")
]
