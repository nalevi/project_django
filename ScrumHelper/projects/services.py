from django.db import models, IntegrityError
from django.shortcuts import get_object_or_404, get_list_or_404, Http404

from projects.stories.models import UserStory
from projects.tasks.models import Task
from projects.epics.models import Epic
from projects.issues.models import Issue

from .models import Project

def get_issues_for_project(project_id):
    '''
    Get all stories/epics/tasks/issues for the current story
    '''
    context = dict()

    
    project = get_object_or_404(Project, pk=project_id)

    if project:
        context['project'] = project
    else:
        raise Http404

    try:
        story_list = get_list_or_404(UserStory, project_code=project.code)
        context['story_list'] = story_list
    except Http404:
        pass

    #task_list = get_list_or_404(Task, project_code=project.code)
    #epic_list = get_list_or_404(Epic, project_code=project.code)
    #issue_list = get_list_or_404(Issue, project_code=project.code)
    try:
        documents_list = project.documents.all()
        context['documents_list'] = documents_list
    except Http404:
        pass


    return context


def delete_project(project_id):
    get_object_or_404(Project, pk=project_id).delete()
    return True