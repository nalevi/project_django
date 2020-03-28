from django.forms import ModelForm
from django import forms
from django.forms.widgets import Select
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

from .models import Project
from projects.stories.models import UserStory
from projects.comments.models import Comment
from projects.epics.models import Epic

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

    '''
    def __init__(self, project_code=None, epic=None,assignee=None, *args, **kwargs):
        super(CreateStoryForm, self).__init__(*args, **kwargs)
        if project_code is not None:
            self.fields["project_code"] = forms.ChoiceField(choices=project_code, widget=forms.Select)
    '''
    

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