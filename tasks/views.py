from django.shortcuts import render, redirect
from tasks.forms import TaskForm, ViewTaskForm
from tasks.models import Task, Role, User, Priority
from django.contrib import messages


def view_tasks(request):
    context = {}
    if not request.user.is_anonymous:
        app_user = User.objects.get(user=request.user)
        context['tasks'] = Task.filter_by_assignee(request.user.id) if app_user.role == Role.EMPLOYEE else (
            Task.filter_by_team(app_user.team)
        )
        context['user'] = app_user

    if request.method == "POST":
        priority = request.POST.get('priority')
        context['tasks'] = context['tasks'].filter(priority=Priority[priority.upper()])

    return render(request, 'tasks/tasks.html', context)


def new_task(request):
    context = {}
    if request.user.is_authenticated:
        logged_user = User.objects.get(user=request.user)
        context = {'user': logged_user}
        if logged_user.is_manager():
            color = 'red'
            if request.method == "POST":
                form = TaskForm(request.user.id, request.POST)
                task_form = form.save(commit=False)
                initial_dict = {'title': task_form.title, 'assignee': task_form.assignee,
                                'priority': task_form.priority, 'status': task_form.status,
                                'description': task_form.description}
                if form.is_valid():
                    try:
                        Task.create_task(task_form.title, task_form.assignee, task_form.created_by, task_form.priority,
                                         task_form.status, task_form.description)
                        messages.success(request, 'Task was added successfully')
                        color = 'green'
                        form = TaskForm(request.user.id)
                    except Exception as e:
                        messages.warning(request, e)
                        form = TaskForm(request.user.id, initial=initial_dict)
                else:
                    messages.warning(request, 'something went wrong')
                    form = TaskForm(request.user.id, initial=initial_dict)
            else:
                form = TaskForm(request.user.id)
            context = {'form': form, 'user': logged_user, 'color': color}
    return render(request, 'tasks/new_task.html', context)


def view_single_task(request, pk):
    if not request.user.is_authenticated:
        return redirect('/')

    user = User.objects.get(user=request.user)
    task = Task.objects.get(pk=pk)
    form = ViewTaskForm(instance=task)

    if request.method == 'POST':
        form = ViewTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            redirect(f'tasks/{pk}', {'user': user})

    return render(request, 'tasks/view_single_task.html', {'form': form, 'task': task, 'user': user})
