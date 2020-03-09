from django.db import models
from django.utils import timezone

from users.models import Profile

from projects.contants import STATE_CHOICES, IMPORTANCE_CHOICES

class Task(models.Model):
    '''
     Task object's model.
    '''
    #id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    name = models.CharField(max_length=50, unique=True, default="Unkown")
    project_code = models.ForeignKey("projects.Project", on_delete=models.CASCADE,to_field="code",related_name="task_project_code")
    created_date = models.DateTimeField(null=False, blank=False,default=timezone.now)
    modified_date = models.DateTimeField(null=False, blank=False,default=timezone.now)
    owner = models.ForeignKey("users.Profile", on_delete=models.CASCADE, related_name="task_owner")
    assignee = models.ForeignKey("users.Profile", on_delete=models.CASCADE, related_name="task_assignee", default="Unkown")
    description = models.CharField(max_length=250, default="Description")
    importance = models.CharField(max_length=8, default="low", choices=IMPORTANCE_CHOICES)
    state = models.CharField(default="OPEN", max_length=15, choices=STATE_CHOICES)


    