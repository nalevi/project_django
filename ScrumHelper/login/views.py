from django.shortcuts import render
from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    redirect_field_name = 'users/index.html'

def index(request):
    return render(request, 'login/index.html')


