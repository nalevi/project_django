from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import datetime, date
from django.contrib.auth.models import User, Group

from projects.stories.services import get_stories_for_user
from projects.epics.services import get_epics_for_user

from worklogs.models import Worklog

from .models import Profile
from .forms import SelectMontForm


def index(request):
    context = {}
    return render(request, 'users/index.html', context)


def detail(request, username):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user_id=user.id)

    context = get_stories_for_user(user.id)

    epics = get_epics_for_user(user.id)

    context.update(epics)

    context['profile'] = profile

    return render(request, 'users/personal_issues.html',context)


def get_users_worklogs(request, username):
    '''
     List the woorklogs in the given month.
    '''
    uid = User.objects.get(username=username).pk
    user = Profile.objects.get(pk=uid)
        
    context = dict()

    if request.method == "POST":
        
        filter_date = datetime.strptime(request.POST.get('month'),"%Y-%m-%d").date()


        try:
            worklogs = Worklog.objects.filter(log_date__month=filter_date.month).filter(log_user=user).order_by('log_date')
            daily_worklogs = worklogs.filter(log_date__day=filter_date.day)
            if worklogs:
                context['daily_worklogs'] = daily_worklogs
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
        now_date = timezone.now()
        worklogs = Worklog.objects.filter(log_date__month=now_date.month).filter(log_user=user).order_by('log_date')
        daily_worklogs = worklogs.filter(log_date__day=now_date.day)
        if worklogs:
            context['daily_worklogs'] = daily_worklogs
            context['worklogs'] = worklogs

        dateForm = SelectMontForm(month=now_date.month)

        context['form'] = dateForm
        return render(request, 'users/worklogs.html', context)

def delete_worklog(request,log_id):
    worklog = Worklog.objects.get(id=log_id)
    profile = worklog.log_user
    worklog.delete()

    return redirect('users:get_users_worklogs', username=profile.user.username)


def team_worklogs(request):
    '''
     List all user's woorklogs of the team (if the current user is in Project manager group or siteadmin) in the given month.
    '''
    users = Profile.objects.all()
    context = dict()
    user_workhours = list()

    if request.method == "POST":
        
        filter_date = datetime.strptime(request.POST.get('month'),"%Y-%m-%d").date()

        if request.user.groups.filter(name=Group(name='project_manager')).exists():

            for u in users:
                workhours = Worklog.objects.filter(log_date__month=filter_date.month).filter(log_user=u)
                logged_hours = 0
                for hours in workhours:
                    logged_hours += hours.logged_hour

                user_workhours.append((u,logged_hours))

            context['user_workhours'] = user_workhours
        else:
            for u in users:
                logged_hours = 0
                if str(u) == str(request.user):
                    workhours = Worklog.objects.filter(log_date__month=filter_date.month).filter(log_user=u)
                    for hours in workhours:
                        logged_hours += hours.logged_hour

                user_workhours.append((u,logged_hours))

            context['user_workhours'] = user_workhours            
            
        dateForm = SelectMontForm()
        context['form'] = SelectMontForm()
        return render(request, 'users/team_worklogs.html', context)

    else:
        now_date = timezone.now()
        if request.user.groups.filter(name=Group(name='project_manager')).exists():

            for u in users:
                workhours = Worklog.objects.filter(log_date__month=now_date.month).filter(log_user=u)
                logged_hours = 0
                for hours in workhours:
                    logged_hours += hours.logged_hour

                user_workhours.append((u,logged_hours))

            context['user_workhours'] = user_workhours
            
        else:
            for u in users:
                logged_hours = 0
                if str(u) == str(request.user):
                    print(u)
                    workhours = Worklog.objects.filter(log_date__month=now_date.month).filter(log_user=u)
                    for hours in workhours:
                        logged_hours += hours.logged_hour

                user_workhours.append((u,logged_hours))

            context['user_workhours'] = user_workhours            

        dateForm = SelectMontForm(month=now_date.month)

        context['form'] = dateForm
        return render(request, 'users/team_worklogs.html', context)