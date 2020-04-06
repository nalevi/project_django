from django.shortcuts import render, redirect, get_object_or_404, Http404

from .models import Epic
from .services import get_epic_details, delete_epic

from projects.forms import CreateEpicForm
from projects.models import Project
from projects.comments.models import Comment

from users.models import Profile

def detail(request, epic_id):
    context = get_epic_details(epic_id)
    return render(request, 'epics/detail.html', context)

def epic_new(request):
    if request.method == "POST":
        form = CreateEpicForm(request.POST)
        if form.is_valid():
            epic = form.save(commit=False)
            owner_prof = Profile.objects.get(user_id=request.user.id)
            epic.owner = owner_prof
            epic.save()
            return redirect('projects:epics:detail', epic_id=epic.id )
    else:
        form = CreateEpicForm()
    return render(request, 'epics/epic_edit.html', {'form': form})


def epic_edit(request, epic_id):
    epic = get_epic_object(epic_id)
    if request.method == "POST":
        form = CreateEpicForm(request.POST, instance=epic)
        if form.is_valid():
            epic = form.save(commit=False)
            epic.save()
            return redirect('projects:epics:detail', epic_id=epic.id )
    else:
        form = CreateEpicForm(instance=epic)
    return render(request, 'epics/epic_edit.html', {'form': form})

def delete(request, epic_id):
    delete_epic(epic_id)

    return render(request, 'users/index.html', {})