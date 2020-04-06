from django.db import models
from django.utils import timezone

from users.models import Profile

from projects.contants import IMPORTANCE_CHOICES, STATE_CHOICES

class Issue(models.Model):
    '''
    Issue object's model.
    '''
    name = models.CharField(max_length=50, unique=True, default="Unkown")
    project_code = models.ForeignKey("projects.Project", on_delete=models.CASCADE,to_field="code",related_name="issue_project_code")
    created_date = models.DateTimeField(null=False, blank=False,default=timezone.now)
    modified_date = models.DateTimeField(null=False, blank=False,default=timezone.now)
    owner = models.ForeignKey("users.Profile", on_delete=models.CASCADE, related_name="issue_owner")
    assignee = models.ForeignKey("users.Profile", on_delete=models.SET_NULL, related_name="issue_assignee", null=True)
    description = models.CharField(max_length=250, default="Description")
    importance = models.CharField(max_length=8, default="low", choices=IMPORTANCE_CHOICES)
    state = models.CharField(default="OPEN", max_length=15, choices=STATE_CHOICES)
    #worklog = 
    defect_type = models.CharField(max_length=10)
    solved = models.BooleanField(default=False)
    solution = models.CharField(max_length=150)
