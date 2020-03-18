from django.shortcuts import render, redirect, get_object_or_404

from .models import UserStory

from projects.forms import CreateStoryForm
from projects.models import Project

from users.models import Profile

def detail(request, story_id):
    story = get_object_or_404(UserStory, pk=story_id)
    proj = get_object_or_404(Project, code=story.project_code.code)
    owner_profile = get_object_or_404(Profile, pk=story.owner.id)
    context ={
        'story': story,
        'proj': proj,
        'owner_profile': owner_profile,
    }
    return render(request, 'stories/detail.html', context)


def story_new(request):
    if request.method == "POST":
        form = CreateStoryForm(request.POST)
        if form.is_valid():
            story = form.save(commit=False)
            story.owner = request.user
            story.save()
            return redirect('projects:stories:detail', story_id=story.id )
    else:
        form = CreateStoryForm()
    return render(request, 'stories/story_edit.html', {'form': form})
