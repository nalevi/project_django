from django.shortcuts import get_object_or_404

from projects.models import Project
from users.models import Profile
from projects.stories.models import UserStory
from projects.comments.models import Comment
from projects.tasks.models import Task

from .models import Epic

def get_epic_object(epic_id):
    return get_object_or_404(Epic, pk=epic_id)

def delete_epic(epic_id):
    get_object_or_404(Epic, pk=epic_id).delete()
    return True



def get_epic_details(epic_id):
    '''
    Get epics details

    context: 
             - stories
             - project
             - owner_profile
             - assignee (optional)
             - tasks
    '''
    epic = get_object_or_404(Epic, pk=epic_id)
    stories = UserStory.objects.filter(epic=epic)
    tasks = Task.objects.filter(epic=epic)
    proj = get_object_or_404(Project, code=epic.project_code.code)
    owner_profile = get_object_or_404(Profile, pk=epic.owner.id)
    context = {
        'epic': epic,
        'stories': stories,
        'tasks': tasks,
        'project': proj,
        'owner_profile': owner_profile,
    }

    return context

def get_epics_for_user(user_id):
    '''
    Get the stories assinged to a specific user

    context: 
             - owner
    '''
    context = dict()

    try:
        owned_user_epics =  Epic.objects.filter(owner=user_id)
        context['epic_owner'] = owned_user_epics
    except Exception:
        pass
    
    
    return context
