from django.shortcuts import render, get_object_or_404, redirect
from django.db import IntegrityError
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import datetime, date
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator

from projects.stories.services import get_stories_for_user
from projects.epics.services import get_epics_for_user
from projects.tasks.services import get_tasks_for_user
from projects.issues.services import get_issues_for_user

from worklogs.models import Worklog

from login.forms import SignUpForm

from .models import Profile
from .forms import SelectMontForm, AddGroupForm


def index(request):
    context = {}
    return render(request, 'users/index.html', context)


def detail(request, username):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user_id=user.id)

    context = get_stories_for_user(user.id)

    epics = get_epics_for_user(user.id)

    context.update(epics)

    tasks = get_tasks_for_user(user.id)

    context.update(tasks)

    issues = get_issues_for_user(user.id)

    context.update(issues)

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

def group_list(request):
    groups_list = Group.objects.all()

    context = {
        'groups_list': groups_list,
    }
    if request.method == "POST":
        groupName = request.POST.get('group')
        if groupName is not None:
            group = Group(name=groupName)
            
            try:
                group.save()

                groups_list = Group.objects.all()

                context['groups_list'] = groups_list
            except IntegrityError:
                context['error_msg'] = "Group already exists"

            form = AddGroupForm()
            context['form'] = form
            return render(request, 'users/groups.html', context)
        else:
            form = AddGroupForm()
            context['form'] = form
            return render(request, 'users/groups.html', context)

    else:
        form = AddGroupForm()
        context['form'] = form
        return render(request, 'users/groups.html', context)

def group_detail(request, gr_id):
    group = get_object_or_404(Group, pk=gr_id)
    permissions = Permission.objects.all()
    groups_permission = group.permissions.all()

    return render(request, 'users/group_detail.html', {'group': group, 
                                                       'permissions':permissions,
                                                       'groups_perm': groups_permission})

def delete_group(request,gr_id):
    Group.objects.get(pk=gr_id).delete()

    return group_list(request)

def add_perm_to_group(request, gr_id, p_id):
    group = get_object_or_404(Group, pk=gr_id)
    permission = get_object_or_404(Permission, pk=p_id)
    group.permissions.add(permission)

    return group_detail(request, gr_id)

def delete_perm_from_group(request, gr_id, p_id):
    group = get_object_or_404(Group, pk=gr_id)
    permission = get_object_or_404(Permission, pk=p_id)
    group.permissions.get(name=permission.name).delete()

    return group_detail(request, gr_id)

def delete_user(request, user_id):
    User.objects.get(pk=user_id).delete()

    return render(request, 'users/index.html', {})

