from django.db import models
from django.utils import timezone

from users.models import Profile
from projects.epics.models import Epic
from projects.contants import IMPORTANCE_CHOICES, STATE_CHOICES 
from projects.comments.models import Comment
from worklogs.models import Worklog

class UserStory(models.Model):
    '''
    UserStory object's model.
    '''
    #id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    name = models.CharField(max_length=50, unique=True, default="Unkown")
    project_code = models.ForeignKey("projects.Project",to_field="code", on_delete=models.CASCADE,related_name="userstory_project_code")
    created_date = models.DateTimeField(null=False, blank=False,default=timezone.now)
    modified_date = models.DateTimeField(null=False, blank=False,default=timezone.now)
    owner = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="userstory_owner")
    assignee = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="userstory_assignee", null=True)
    description = models.CharField(max_length=250, default="Description")
    importance = models.CharField(max_length=8, default="low", choices=IMPORTANCE_CHOICES)
    state = models.CharField(default="OPEN", max_length=15, choices=STATE_CHOICES)
    epic = models.ForeignKey("epics.Epic", on_delete=models.CASCADE, related_name="userstory_epic", null=True)
    acceptance = models.CharField(max_length=50, null=True)
    comment = models.ManyToManyField("comments.Comment", related_name="userstory_comment")
    work_log = models.ManyToManyField("worklogs.Worklog")

    def __str__(self):
        return self.name