from django.shortcuts import render
from tasks.models import Task


def homepage(request):
	context = {
		'tasks': Task.objects.all()
	}
	return render(request, 'homepage.html', context)
