from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse

from projects.stories.services import get_stories_for_user

from .models import Profile, User

def index(request):
    context = {}
    return render(request, 'users/index.html', context)

def detail(request, user_id):
    context = get_stories_for_user(user_id)

    return render(request, 'users/personal_issues.html',context)
