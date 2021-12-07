from django.urls import path
from . import views

urlpatterns = [
    path('tasks/<str:pk>', views.view_single_task, name="view_single_task")
]
