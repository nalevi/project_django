from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    group = forms.ChoiceField(widget=forms.Select,choices=[ (group, group.name) for group in Group.objects.all()])

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'group' )