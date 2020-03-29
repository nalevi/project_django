from django.forms import ModelForm
from django import forms
from django.forms.widgets import Select
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.admin import widgets                                       

from .models import Project
from projects.stories.models import UserStory
from projects.comments.models import Comment
from projects.epics.models import Epic

from worklogs.models import Worklog


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

    project_code = forms.ModelChoiceField(widget=forms.Select,queryset=Project.objects.all())
    epic = forms.ModelChoiceField(widget=forms.Select, queryset=Epic.objects.all(), required=False)
    assignee = forms.ModelChoiceField(widget=forms.Select, queryset=User.objects.all(), required=False)
    

    class Meta:
        model = UserStory
        fields = ['name', 'project_code',
                  'assignee', 'description', 'importance', 'epic']
        labels = {
            'project_code': _('Project\'s code'),
        }
        
   


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']



class CreateEpicForm(ModelForm):

    project_code = forms.ModelChoiceField(widget=forms.Select,queryset=Project.objects.all())
    class Meta:
        model = Epic
        fields = ['name', 'project_code',
                  'description']
        labels = {
            'project_code': _('Project\'s code'),
        }


class CreateWorklogform(ModelForm):

    class Meta:
        model = Worklog
        fields = ['log_date', 'logged_hour']

    def __init__(self, *args, **kwargs):
        super(CreateWorklogform, self).__init__(*args, **kwargs)
        self.fields['log_date'].widget = widgets.AdminDateWidget()