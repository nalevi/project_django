from django.shortcuts import render, redirect, get_object_or_404, Http404

from .models import UserStory
from .services import get_story_details, get_story_object

from projects.forms import CreateStoryForm, CommentForm
from projects.models import Project
from projects.comments.models import Comment

from users.models import Profile

def detail(request, story_id):
    context = get_story_details(story_id)
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


def story_edit(request, story_id):
    story = get_story_object(story_id)
    if request.method == "POST":
        form = CreateStoryForm(request.POST, instance=story)
        if form.is_valid():
            story = form.save(commit=False)
            story.save()
            return redirect('projects:stories:detail', story_id=story.id )
    else:
        form = CreateStoryForm(instance=story)
    return render(request, 'stories/story_edit.html', {'form': form})


def create_comment(request, story_id):
    if request.method == "POST":
        comment_text = request.POST.get('comment_txt', None)
        try:
            comment = Comment(text=comment_text, owner=request.user, owner_usr=request.user.username)
            comment.save()

            story = UserStory.objects.get(pk=story_id)
            story.comment.add(comment)
            story.save()
            return redirect('projects:stories:detail', story_id=story.id )
        except Exception:
            return redirect('projects:stories:detail', story_id=story.id )
    else:
        return render(request, 'stories/story_edit.html', {'form': form})

def get_story_comments(request, story_id):
    return

def delete_comment(request):
    return