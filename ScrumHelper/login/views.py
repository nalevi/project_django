from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout

class CustomLoginView(LoginView):
    redirect_field_name = 'users/index.html'

def index(request):
    return render(request, 'login/index.html')

def logout(request):
    logout(request)
    return redirect('login:login')


