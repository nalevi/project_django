from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse

from projects.stories.services import get_stories_for_user
from projects.epics.services import get_epics_for_user

from worklogs.models import Worklog

from .models import Profile, User


def index(request):
    context = {}
    return render(request, 'users/index.html', context)

def detail(request, username):
    user_id = User.objects.get(username=username).pk

    context = get_stories_for_user(user_id)

    epics = get_epics_for_user(user_id)

    context.update(epics)

    return render(request, 'users/personal_issues.html',context)

def get_users_worklogs(request, username):
    uid = User.objects.get(username=username).pk
    user = Profile.objects.get(pk=uid)

    worklogs = user.work_log.all()

    context = {
        'user': user,
        'worklogs': worklogs
    }

    return render(request, 'users/worklogs.html', context)

def delete_worklog(request,log_id):
    profile = Profile.objects.get(user_id=request['user'].id)

    profile.work_log.get(worklog_id=log_id).delete()

    return redirect('users:get_users_worklogs', uid=profile.user.id)
