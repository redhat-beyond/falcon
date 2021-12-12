from django.shortcuts import render, redirect
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
        form = TaskForm(request.user.id, request.POST)
        taskForm = form.save(commit=False)
        if form.is_valid():
            try:
                Task.create_task(taskForm.title, taskForm.created_by, taskForm.assignee, taskForm.priority,
                                 taskForm.status, taskForm.description)

                messages.success(request, 'Task was added successfully')
                form = TaskForm(request.user.id)
            except Exception as e:
                messages.warning(request, e)
                form = TaskForm(request.user.id,
                                initial={'title': taskForm.title, 'assignee': taskForm.assignee,
                                         'priority': taskForm.priority, 'status': taskForm.status,
                                         'description': taskForm.description})
        else:
            messages.warning(request, 'something went wrong')
            form = TaskForm(request.user.id,
                            initial={'title': taskForm.title, 'priority': taskForm.priority, 'status': taskForm.status,
                                     'description': taskForm.description, 'assignee': taskForm.assignee, })
    else:
        form = TaskForm(request.user.id)

    return render(request, 'new_task.html', {'form': form})


def view_single_task(request, pk):
    if not request.user.is_authenticated:
        return redirect('/')

    user = User.objects.get(user=request.user)
    task = Task.objects.get(pk=pk)
    form = TaskForm(instance=task)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            redirect(f'tasks/{pk}', {'user': user})

    return render(request, 'tasks/view_single_task.html', {'form': form, 'task': task, 'user': user})