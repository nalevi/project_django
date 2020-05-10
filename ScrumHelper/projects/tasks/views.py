from django.shortcuts import render, redirect, get_object_or_404, Http404
from django.contrib.auth.decorators import permission_required

from .models import Task
from .services import get_task_details, get_task_object, delete_task, change_task_state

from projects.forms import CreateTaskForm, CommentForm, CreateWorklogform
from projects.models import Project
from projects.comments.models import Comment

from users.models import Profile

def detail(request, task_id):
    context = get_task_details(task_id)
    return render(request, 'tasks/detail.html', context)


def task_new(request):
    if request.method == "POST":
        form = CreateTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user
            task.save()
            return redirect('projects:tasks:detail', task_id=task.id )
    else:
        form = CreateTaskForm()
    return render(request, 'tasks/task_edit.html', {'form': form})


def task_edit(request, task_id):
    task = get_task_object(task_id)
    if request.method == "POST":
        form = CreateTaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            return redirect('projects:tasks:detail', task_id=task.id )
    else:
        form = CreateTaskForm(instance=task)
    return render(request, 'tasks/task_edit.html', {'form': form})


def create_comment(request, task_id):
    if request.method == "POST":
        comment_text = request.POST.get('comment_txt', None)
        task = Task.objects.get(pk=task_id)

        try:
            comment = Comment(text=comment_text, owner=request.user)
            comment.save()

            task.comment.add(comment)
            task.save()
            return redirect('projects:tasks:detail', task_id=task.id )
        except Exception:
            raise Http404



def delete_comment(request, task_id,comment_id):    
    task = get_task_object(task_id)
    try:
        Comment.objects.get(pk=comment_id).delete()
    except Exception:
        raise Http404

    return redirect('projects:tasks:detail', task_id=task_id )


def delete(request, task_id):
    success = delete_task(task_id=task_id)

    if success:
        return redirect('users:index')

def change_state(request, task_id):
    succes = change_task_state(task_id)

    return redirect('projects:tasks:detail', task_id=task_id)
    

def add_worklog(request, task_id):
    if request.method == "POST":
        form = CreateWorklogform(request.POST)
        task = Task.objects.get(pk=task_id)

        if form.is_valid():
            worklog = form.save(commit=False)
            prof = get_object_or_404(Profile, user_id=request.user.id)
            worklog.log_user = prof

            worklog.save()

            task.work_log.add(worklog)
            task.save()
            return redirect('projects:tasks:detail', task_id=task.id )
        else:
            form = CreateWorklogform()
            error_msg = "Not a valid date time. Please use Year-Month-Day format (Example: 2020-12-01)."
            return render(request, 'worklogs/log_work.html', {'form': form, 'error_msg': error_msg})


    else:
        form = CreateWorklogform()
        return render(request, 'worklogs/log_work.html', {'form': form})