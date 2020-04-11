'''
    Services for the views to communicate with the database layer
'''
from django.shortcuts import get_object_or_404

from projects.models import Project
from users.models import Profile
from projects.epics.models import Epic
from projects.comments.models import Comment


from .models import Issue

def get_issue_object(issue_id):
    '''
    Simply get the issue object from the database
    '''

    return get_object_or_404(Issue, pk=issue_id)

def get_issue_details(issue_id):
    '''
    Get stories details

    context: 
             - issue
             - proj
             - owner_profile
             - assignee (optional)
             - epic (optional)
             - comments
             - work_logs
    '''
    issue = get_object_or_404(Issue, pk=issue_id)
    proj = get_object_or_404(Project, code=issue.project_code.code)
    owner_profile = get_object_or_404(Profile, pk=issue.owner.id)
    context = {
        'issue': issue,
        'proj': proj,
        'owner_profile': owner_profile,
    }
    
    try:
        assignee_profile = get_object_or_404(Profile, pk=issue.assignee.id)
        context['assignee'] = assignee_profile
    except Exception:
        pass

    try:
        epic_link = get_object_or_404(Epic, pk=issue.epic.id)
        context['epic'] = epic_link
    except Exception:
        pass
    
    comments = issue.comment.all()
    if comments:
        context['comments'] = comments

    logs = issue.work_log.all()
    if logs:
        context['worklogs'] = logs

    return context

def get_issues_for_user(user_id):
    '''
    Get the issues assinged to a specific user

    context: 
             - assigned_to
             - owner
    '''
    context = dict()

    try:
        assigned_user_issues = Issue.objects.filter(assignee=user_id)
        context['assigned_issues'] = assigned_user_issues
    except Exception:
        pass    
    
    context['profile'] = Profile.objects.get(pk=user_id)

    return context


def delete_issue(issue_id):
    get_object_or_404(Issue, pk=issue_id).delete()
    return True

def change_issue_state(issue_id):
    issue = get_object_or_404(Issue, pk=issue_id)

    if issue.state == 'OPEN':
        issue.state = 'IN PROGRESS'
    elif issue.state == 'IN PROGRESS':
        issue.state = 'TESTING'
    elif issue.state == 'TESTING':
        issue.state = 'DONE'
    elif issue.state == 'DONE':
        issue.state = 'CLOSED'
    elif issue.state == 'CLOSED':
        issue.state = 'OPEN'

    try:
        issue.save()
        return True
    except Exception:
        return False
    
    return False
