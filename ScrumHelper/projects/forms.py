from django.forms import ModelForm
from django import forms
from django.forms.widgets import Select
from django.utils.translation import gettext_lazy as _

from .models import Project
from projects.stories.models import UserStory

class CreateProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'code']
        labels = {
            'name': _('Project name'),
            'code': _('Project code'),
        }
        help_texts = {
            'code': _('A maximum of 6 charachter length')
        }
        

class CreateStoryForm(ModelForm):

    project_code = forms.ChoiceField(widget=forms.Select,choices=[(proj.id,proj.code) for proj in Project.objects.all()])
    class Meta:
        model = UserStory
        fields = ['name', 'project_code',
                  'assignee', 'description', 'importance', 'epic']
        labels = {
            'project_code': _('Project\'s code'),
        }
        