from django.db import models, IntegrityError
from django.shortcuts import get_object_or_404, get_list_or_404

from projects.stories.models import UserStory
from projects.tasks.models import Task
from projects.epics.models import Epic
from projects.issues.models import Issue

from .models import Project

def get_issues_for_project(project_id):
    '''
    Get all stories/epics/tasks/issues for the current story
    '''
    project = get_object_or_404(Project, pk=project_id)

    story_list = get_list_or_404(UserStory, project_code=project.code)
    #task_list = get_list_or_404(Task, project_code=project.code)
    #epic_list = get_list_or_404(Epic, project_code=project.code)
    #issue_list = get_list_or_404(Issue, project_code=project.code)
    documents_list = project.documents.all()
    context = {
        'project': project,
        'story_list': story_list,
        #'task_list': task_list,
        #'epic_list': epic_list,
        #'issue_list': issue_list
        'documents_list': documents_list,
    }


    return context


def delete_project(project_id):
    get_object_or_404(Project, pk=project_id).delete()
    return True