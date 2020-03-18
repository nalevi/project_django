'''
    Services for the views to communicate with the database layer
'''
from django.shortcuts import get_object_or_404

from projects.models import Project
from users.models import Profile
from projects.epics.models import Epic

from .models import UserStory

def get_story_object(story_id):
    return get_object_or_404(UserStory, pk=story_id)

def get_story_details(story_id):
    story = get_object_or_404(UserStory, pk=story_id)
    proj = get_object_or_404(Project, code=story.project_code.code)
    owner_profile = get_object_or_404(Profile, pk=story.owner.id)
    context = {
        'story': story,
        'proj': proj,
        'owner_profile': owner_profile,
    }
    
    try:
        assignee_profile = get_object_or_404(Profile, pk=story.assignee.id)
        context['assignee'] = assignee_profile
    except Exception:
        return context

    try:
        epic_link = get_object_or_404(Epic, pk=story.epic.id)
        context['epic'] = epic_link
    except Exception:
        return context
    

    return context