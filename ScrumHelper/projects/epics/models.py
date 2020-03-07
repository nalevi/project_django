from django.db import models
from django.utils import timezone

from users.models import Profile

class Epic(models.Model):
    '''
    Epic object's model.
    '''
    name = models.CharField(max_length=50, unique=True, default="Unkown")
    project_code = models.ForeignKey("projects.Project", on_delete=models.CASCADE,to_field="code",related_name="epic_project_code")
    created_date = models.DateTimeField(null=False, blank=False,default=timezone.now)
    modified_date = models.DateTimeField(null=False, blank=False,default=timezone.now)
    owner = models.ForeignKey("users.Profile", on_delete=models.CASCADE, related_name="epic_owner")
    assignee = models.ForeignKey("users.Profile", on_delete=models.CASCADE, related_name="epic_assignee", default="Unkown")
    description = models.CharField(max_length=250, default="Description")



