from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.db import IntegrityError

from .forms import SignUpForm

class CustomLoginView(LoginView):
    redirect_field_name = 'users/index.html'

def index(request):
    return render(request, 'login/index.html')

def logout(request):
    logout(request)
    return redirect('login:login')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except IntegrityError:
                error_msg = "Can't create user"
                form = SignUpForm()
                return render(request, 'registration/signup.html', {'form': form, 'error_msg': error_msg} )
                
            return redirect('users:index')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def edit_user(request,user_id):
    user = User.objects.get(pk=user_id)
    if request.method == 'POST':
        form = SignUpForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
                
            return redirect('users:index')
    else:
        form = SignUpForm(instance=user)
    return render(request, 'registration/signup.html', {'form': form})

def change_pw(request, user_id):
    user = User.objects.get(pk=user_id)
    if request.method == 'POST':
        form = SignUpForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('users:detail', user.username)
    else:
        form = SignUpForm(instance=user)
    return render(request, 'registration/signup.html', {'form': form})
