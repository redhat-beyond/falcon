from django.urls import path
from tasks import views

urlpatterns = [
    path('tasks/', views.view_tasks, name='tasks'),
    path('tasks/create', views.new_task, name='new_task'),
    path('tasks/<str:pk>', views.view_single_task, name="view_single_task"),
    path('tasks/edit/<str:pk>', views.edit_single_task, name="edit_task"),
    path('tasks/delete/<str:pk>', views.delete_task, name="delete_task"),

]
