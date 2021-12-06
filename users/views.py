from django.shortcuts import redirect
from django.contrib.auth import views as auth_views


def login(request):
    if(request.user.is_authenticated):
        return redirect('/')
    else:
        return auth_views.LoginView.as_view(template_name='users/login.html')(request)


def logout(request):
    return auth_views.LogoutView.as_view(template_name='users/logout.html')(request)
