'''
    Services for the views to communicate with the database layer
'''
from django.shortcuts import get_object_or_404

from projects.models import Project
from users.models import Profile
from projects.epics.models import Epic
from projects.comments.models import Comment


from .models import Task

def get_task_object(task_id):
    '''
    Simply get the task object from the database
    '''

    return get_object_or_404(Task, pk=task_id)

def get_task_details(task_id):
    '''
    Get stories details

    context: 
             - task
             - proj
             - owner_profile
             - assignee (optional)
             - epic (optional)
             - comments
             - work_logs
    '''
    task = get_object_or_404(Task, pk=task_id)
    proj = get_object_or_404(Project, code=task.project_code.code)
    owner_profile = get_object_or_404(Profile, pk=task.owner.id)
    context = {
        'task': task,
        'proj': proj,
        'owner_profile': owner_profile,
    }
    
    try:
        assignee_profile = get_object_or_404(Profile, pk=task.assignee.id)
        context['assignee'] = assignee_profile
    except Exception:
        pass

    try:
        epic_link = get_object_or_404(Epic, pk=task.epic.id)
        context['epic'] = epic_link
    except Exception:
        pass
    
    comments = task.comment.all()
    if comments:
        context['comments'] = comments

    logs = task.work_log.all()
    if logs:
        context['worklogs'] = logs

    return context

def get_tasks_for_user(user_id):
    '''
    Get the stories assinged to a specific user

    context: 
             - assigned_to
             - owner
    '''
    context = dict()

    try:
        assigned_user_tasks = Task.objects.filter(assignee=user_id)
        context['assigned_tasks'] = assigned_user_tasks
    except Exception:
        pass    
    
    context['profile'] = Profile.objects.get(pk=user_id)

    return context


def delete_task(task_id):
    get_object_or_404(Task, pk=task_id).delete()
    return True

def change_task_state(task_id):
    task = get_object_or_404(Task, pk=task_id)

    if task.state == 'OPEN':
        task.state = 'DONE'
    elif task.state == 'DONE':
        task.state = 'CLOSED'
    elif task.state == 'CLOSED':
        task.state = 'OPEN'

    try:
        task.save()
        return True
    except Exception:
        return False
    
    return False
