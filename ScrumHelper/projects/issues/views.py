from django.shortcuts import render, redirect, get_object_or_404, Http404
from django.contrib.auth.decorators import permission_required

from .models import Issue
from .services import get_issue_details, get_issue_object, delete_issue, change_issue_state

from projects.forms import CreateIssueForm, CommentForm, CreateWorklogform
from projects.models import Project
from projects.comments.models import Comment

from users.models import Profile

def detail(request, issue_id):
    context = get_issue_details(issue_id)
    return render(request, 'issues/detail.html', context)


def issue_new(request):
    if request.method == "POST":
        form = CreateIssueForm(request.POST)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.owner = request.user
            issue.save()
            return redirect('projects:issues:detail', issue_id=issue.id )
    else:
        form = CreateIssueForm()
    return render(request, 'issues/issue_edit.html', {'form': form})


def issue_edit(request, issue_id):
    issue = get_issue_object(issue_id)
    if request.method == "POST":
        form = CreateIssueForm(request.POST, instance=issue)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.save()
            return redirect('projects:issues:detail', issue_id=issue.id )
    else:
        form = CreateIssueForm(instance=issue)
    return render(request, 'issues/issue_edit.html', {'form': form})


def create_comment(request, issue_id):
    if request.method == "POST":
        comment_text = request.POST.get('comment_txt', None)
        issue = Issue.objects.get(pk=issue_id)

        try:
            comment = Comment(text=comment_text, owner=request.user)
            comment.save()

            issue.comment.add(comment)
            issue.save()
            return redirect('projects:issues:detail', issue_id=issue.id )
        except Exception:
            raise Http404
    


def delete_comment(request, issue_id,comment_id):    
    issue = get_issue_object(issue_id)
    try:
        Comment.objects.get(pk=comment_id).delete()
    except Exception:
        raise Http404

    return redirect('projects:issues:detail', issue_id=issue_id )


def delete(request, issue_id):
    success = delete_issue(issue_id=issue_id)

    if success:
        return redirect('users:index')

def change_state(request, issue_id):
    succes = change_issue_state(issue_id)

    return redirect('projects:issues:detail', issue_id=issue_id)
    

def add_worklog(request, issue_id):
    if request.method == "POST":
        form = CreateWorklogform(request.POST)
        issue = Issue.objects.get(pk=issue_id)

        if form.is_valid():
            worklog = form.save(commit=False)
            prof = get_object_or_404(Profile, user_id=request.user.id)
            worklog.log_user = prof

            worklog.save()

            issue.work_log.add(worklog)
            issue.save()
            return redirect('projects:issues:detail', issue_id=issue.id )
        else:
            form = CreateWorklogform()
            error_msg = "Not a valid date time. Please use Year-Month-Day format (Example: 2020-12-01)."
            return render(request, 'worklogs/log_work.html', {'form': form, 'error_msg': error_msg})


    else:
        form = CreateWorklogform()
        return render(request, 'worklogs/log_work.html', {'form': form})