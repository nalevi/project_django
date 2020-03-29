from django.shortcuts import render, redirect, get_object_or_404, Http404
from django.contrib.auth.decorators import permission_required

from .models import UserStory
from .services import get_story_details, get_story_object, delete_story, change_story_state

from projects.forms import CreateStoryForm, CommentForm, CreateWorklogform
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
        story = UserStory.objects.get(pk=story_id)

        try:
            comment = Comment(text=comment_text, owner=request.user)
            comment.save()

            story.comment.add(comment)
            story.save()
            return redirect('projects:stories:detail', story_id=story.id )
        except Exception:
            raise Http404
    else:
        return render(request, 'stories/story_edit.html', {'form': form})


def delete_comment(request, story_id,comment_id):    
    story = get_story_object(story_id)
    try:
        Comment.objects.get(pk=comment_id).delete()
    except Exception:
        raise Http404

    return redirect('projects:stories:detail', story_id=story_id )


def delete(request, story_id):
    success = delete_story(story_id=story_id)

    if success:
        return redirect('users:index')

def change_state(request, story_id):
    succes = change_story_state(story_id)

    return redirect('projects:stories:detail', story_id=story_id)
    

def add_worklog(request, story_id):
    if request.method == "POST":
        form = CreateWorklogform(request.POST)
        story = UserStory.objects.get(pk=story_id)

        print(form.fields['log_date'])
        if form.is_valid():
            worklog = form.save(commit=False)
            prof = get_object_or_404(Profile, user_id=request.user.id)
            worklog.log_user = prof

            

            worklog.save()

            story.work_log.add(worklog)
            story.save()
            return redirect('projects:stories:detail', story_id=story.id )

    else:
        form = CreateWorklogform()
        return render(request, 'worklogs/log_work.html', {'form': form})