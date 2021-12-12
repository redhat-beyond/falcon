from django.shortcuts import render
from tasks.models import Task
from users.models import Role, User


def view_tasks(request):
    context = {}
    if not request.user.is_anonymous:
        app_user = User.objects.get(user=request.user)
        context['tasks'] = Task.filter_by_assignee(request.user.id) if app_user.role == Role.EMPLOYEE else (
            Task.filter_by_team(app_user.team)
        )
        context['user'] = app_user
    return render(request, 'tasks/tasks.html', context)
