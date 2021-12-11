from django.shortcuts import render
from django.shortcuts import redirect, render
from tasks.forms import TaskForm
from tasks.models import Task, Role, User
from django.contrib import messages


def view_tasks(request):
    context = {}
    if not request.user.is_anonymous:
        app_user = User.objects.get(user=request.user)
        context['tasks'] = Task.filter_by_assignee(request.user.id) if app_user.role == Role.EMPLOYEE else (
            Task.filter_by_team(app_user.team)
        )
        context['user'] = app_user
    return render(request, 'tasks/tasks.html', context)


def new_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            taskForm = form.save(commit=False)
            try:
                Task.create_task(taskForm.title, taskForm.assignee, taskForm.created_by, taskForm.priority,
                                 taskForm.status, taskForm.description)
                messages.success(request, 'Task was added successfully')
                form = TaskForm(request.user.id)
                redirect('new_task')
            except Exception as e:
                messages.warning(request, e)
                form = TaskForm(request.user.id,
                                initial={'title': taskForm.title, 'assignee': taskForm.assignee,
                                         'priority': taskForm.priority, 'status': taskForm.status,
                                         'description': taskForm.description})
    else:
        form = TaskForm(request.user.id)

    return render(request, 'new_task.html', {'form': form})
