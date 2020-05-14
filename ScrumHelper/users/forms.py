from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User, Group
from django.contrib.admin import widgets
from django.forms.widgets import Widget, Select
from django.utils.dates import MONTHS
from django.utils.safestring import mark_safe

import datetime
import re


class SelectMontForm(forms.Form):

    month = forms.DateField()

    fields = ['month']
    labels = {
        'month': _('Display logs this month')
    }

    def __init__(self,month=None, *args, **kwargs):
        super(SelectMontForm, self).__init__(*args, **kwargs)
        self.fields['month'].widget = widgets.AdminDateWidget()
        if month is not None:
            self.month = month

class AddGroupForm(forms.Form):
    
    group = forms.CharField()

    fields = ['group']
    labels = {
        'group': 'Group\'s name'
    }

class AddUserToGroup(forms.Form):

    groups = forms.ChoiceField(widget=forms.Select,
                              choices=[ (group, group.name) for group in Group.objects.all()],
                              required=False)

    fields = ['groups']
    labels = {
        'groups': 'Add to group'
    }