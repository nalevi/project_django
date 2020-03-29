from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
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

    def __init__(self, *args, **kwargs):
        super(SelectMontForm, self).__init__(*args, **kwargs)
        self.fields['month'].widget = widgets.AdminDateWidget()