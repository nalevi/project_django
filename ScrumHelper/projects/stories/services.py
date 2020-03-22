'''
    Services for the views to communicate with the database layer
'''
from django.shortcuts import get_object_or_404

from projects.models import Project
from users.models import Profile
from projects.epics.models import Epic
from projects.comments.models import Comment

from .models import UserStory

def get_story_object(story_id):
    '''
    Simply get the story object from the database
    '''

    return get_object_or_404(UserStory, pk=story_id)

def get_story_details(story_id):
    '''
    Get stories details

    context: 
             - story
             - proj
             - owner_profile
             - assignee (optional)
             - epic (optional)
             - comments
    '''
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
        pass

    try:
        epic_link = get_object_or_404(Epic, pk=story.epic.id)
        context['epic'] = epic_link
    except Exception:
        pass
    
    comments = story.comment.all()
    context['comments'] = comments

    return context

def get_stories_for_user(user_id):
    '''
    Get the stories assinged to a specific user

    context: 
             - assigned_to
             - owner
    '''
    context = dict()

    try:
        assigned_user_stories = UserStory.objects.filter(assignee=user_id)
        context['assigned_to'] = assigned_user_stories
    except Exception:
        pass

    try:
        owned_user_stories =  UserStory.objects.filter(owner=user_id).exclude(assignee=user_id)
        context['owner_of'] = owned_user_stories
    except Exception:
        pass
    
    
    return context


def delete_story(story_id):
    get_object_or_404(UserStory, pk=story_id).delete()
    return True