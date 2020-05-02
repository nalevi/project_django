from django.forms import ModelForm
from django import forms
from django.forms.widgets import Select
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.admin import widgets   
from django.core.exceptions import ValidationError
from datetime import datetime                                    

from .models import Project
from .stories.models import UserStory
from .comments.models import Comment
from .epics.models import Epic
from .tasks.models import Task
from .issues.models import Issue
from .contants import ISSUE_CHOICES

from worklogs.models import Worklog

def input_date_validator(date_value):
    try:
        datetime.strptime(date_value, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")

class CreateProjectForm(ModelForm):
    release = forms.CharField(required=False)

    class Meta:
        model = Project
        fields = ['name', 'code', 'release']
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

    logged_hour = forms.IntegerField(max_value=8, min_value=1)
    log_date = forms.DateField(input_formats=['%Y-%m-%d'])
    
    class Meta:
        model = Worklog
        fields = ['log_date', 'logged_hour']

    def __init__(self, *args, **kwargs):
        super(CreateWorklogform, self).__init__(*args, **kwargs)
        self.fields['log_date'].widget = widgets.AdminDateWidget()

class CreateTaskForm(ModelForm):

    project_code = forms.ModelChoiceField(widget=forms.Select,queryset=Project.objects.all())
    epic = forms.ModelChoiceField(widget=forms.Select, queryset=Epic.objects.all(), required=False)
    assignee = forms.ModelChoiceField(widget=forms.Select, queryset=User.objects.all(), required=False)
    

    class Meta:
        model = Task
        fields = ['name', 'project_code',
                  'assignee', 'description', 'importance', 'epic']
        labels = {
            'project_code': _('Project\'s code'),
        }

class CreateIssueForm(ModelForm):

    project_code = forms.ModelChoiceField(widget=forms.Select,queryset=Project.objects.all())
    epic = forms.ModelChoiceField(widget=forms.Select, queryset=Epic.objects.all(), required=False)
    assignee = forms.ModelChoiceField(widget=forms.Select, queryset=User.objects.all(), required=False)
    defect_type = forms.ChoiceField(widget=forms.Select, choices=ISSUE_CHOICES)
    solution = forms.CharField(required=False)
    

    class Meta:
        model = Issue
        fields = ['name', 'project_code',
                  'assignee', 'description', 'importance', 'epic', 'defect_type', 'solution']
        labels = {
            'project_code': _('Project\'s code'),
        }