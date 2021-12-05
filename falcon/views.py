from django.shortcuts import redirect, render

from users.models import User


def homepage(request):
    if(request.user.is_staff):
        return redirect('/admin')

    if(request.user.is_authenticated):
        user = User.objects.get(user=request.user)
        return render(request, 'homepage.html', {'user': user})

    return render(request, 'homepage.html')