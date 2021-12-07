from django.shortcuts import render, redirect
from tasks.models import Task
from .forms import TaskForm
from users.models import User


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
