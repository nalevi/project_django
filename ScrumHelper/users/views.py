from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse

from .models import Profile, User

def index(request):
    users_list = User.objects.all()
    context = {
        'users_list': users_list,
    }
    return render(request, 'users/index.html', context)

def detail(request, user_id):
    user_full_name = Profile.objects.get(user_id=user_id).getFullName()
    return HttpResponse("Hello user %s. " % user_full_name)
