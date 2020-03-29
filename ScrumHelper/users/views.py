from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils.translation import gettext_lazy as _
from datetime import datetime

from projects.stories.services import get_stories_for_user
from projects.epics.services import get_epics_for_user

from worklogs.models import Worklog

from .models import Profile, User
from .forms import SelectMontForm


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
    '''
     List the woorklogs in the given month.
    '''
    if request.method == "POST":
        
        filter_date = datetime.strptime(request.POST.get('month'),"%Y-%m-%d").date()
        uid = User.objects.get(username=username).pk
        user = Profile.objects.get(pk=uid)

        context = dict()

        try:
            worklogs = Worklog.objects.filter(log_date__month=filter_date.month).filter(log_user=user).order_by('log_date')
            if worklogs:
                context['worklogs'] = worklogs
            else:
                raise Http404

            dateForm = SelectMontForm()
            context['form'] = SelectMontForm()
            return render(request, 'users/worklogs.html', context)
            
        except Http404:
            dateForm = SelectMontForm()
            return render(request, 'users/worklogs.html', {'form': dateForm })

    else:
        dateForm = SelectMontForm()
        return render(request, 'users/worklogs.html', {'form': dateForm })

def delete_worklog(request,log_id):
    worklog = Worklog.objects.get(id=log_id)
    profile = worklog.log_user
    worklog.delete()

    return redirect('users:get_users_worklogs', username=profile.user.username)
