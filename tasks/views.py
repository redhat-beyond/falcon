from django.shortcuts import render, redirect
from tasks.forms import CommentForm, TaskForm, ViewTaskForm
from tasks.models import Task, Role, User, Priority, Status, Comment
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
        status = request.POST.get('status')

        if status == 'InProgress':
            status = 'in_progress'

        if status == "" and priority != "":
            context['tasks'] = context['tasks'].filter(priority=Priority[priority.upper()])
        elif priority == "" and status != "":
            context['tasks'] = context['tasks'].filter(status=Status[status.upper()])
        elif priority != "" and status != "":
            context['tasks'] = context['tasks'].filter(status=Status[status.upper()])
            context['tasks'] = context['tasks'].filter(priority=Priority[priority.upper()])

    return render(request, 'tasks/tasks.html', context)


def new_task(request):
    context = {'not_auth_user': ''}
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
    task_form = ViewTaskForm(instance=task)
    comment_form = CommentForm(user, task)
    task_creator = User.objects.get(user=task.created_by)
    if user.team.id != task_creator.team.id:
        return redirect('/')
    if request.method == 'POST':
        if 'taskSubmit' in request.POST:
            task_form = ViewTaskForm(request.POST, instance=task)
            if task_form.is_valid():
                task_form.save()
        elif 'commentSubmit' in request.POST:
            comment_form = CommentForm(user, task, request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.appUser = user
                new_comment.task = task
                new_comment.title = f"task id: {task.id}, commented by: {user.user.username}"
                new_comment.save()
                comment_form = CommentForm(user, task)

        redirect(f'tasks/{pk}', {'user': user})

    return render(request,
                  'tasks/view_single_task.html',
                  {'task_form': task_form, 'comment_form': comment_form, 'task': task, 'user': user})


def edit_single_task(request, pk):
    context = {}
    if request.user.is_authenticated:
        logged_user = User.objects.get(user=request.user)
        context = {'user': logged_user, 'auth': False}
        task = Task.objects.get(id=pk)
        task_creator = User.objects.get(user=task.created_by)
        if logged_user.is_manager() and task_creator.team.id == logged_user.team.id:
            task = Task.objects.get(id=pk)
            form = TaskForm(request.user.id, instance=task)
            logged_user = User.objects.get(user=request.user)
            color = 'red'
            if request.method == "POST":
                success = update_task(request, task)
                form = TaskForm(request.user.id, instance=task)
                if success:
                    return redirect(f'/tasks/{pk}', {'user': logged_user})
            context = {'form': form, 'user': logged_user, 'color': color, 'auth': True}

    return render(request, 'tasks/edit_task.html/', context)


def update_task(request, task):
    form = TaskForm(request.user.id, request.POST, instance=task)
    task_form = form.save(commit=False)
    success = False
    if form.is_valid():
        try:
            if task_validate(task_form):
                form.save()
                success = True
        except Exception as e:
            messages.warning(request, e)
    return success


def task_validate(task):
    if task.title == "":
        raise ValueError("Title must contain at lease one character")
    assigner_role = task.created_by.role
    assigner_team = task.created_by.team
    assignee_team = task.assignee.team
    if assignee_team != assigner_team:
        raise ValueError("Manager can assign tasks only for his own employees")
    if assigner_role != Role.MANAGER:
        raise ValueError("User must be a manager to assign tasks")
    return True


def delete_task(request, pk):
    if not request.user.is_authenticated:
        return redirect('/')
    user = User.objects.get(user=request.user)
    if not user.is_manager():
        return redirect('/')
    task = Task.objects.get(pk=pk)
    task_creator = User.objects.get(user=task.created_by)
    if user.team.id != task_creator.team.id:
        return redirect('/')
    task.delete()
    Comment.objects.filter(task_id=task.id).delete()
    return redirect('tasks')
