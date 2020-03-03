from django.db import models
from django.utils import timezone

from users.models import Profile

class Project(models.Model):
    """
        Project object's model class.
    """
    id = models.IntegerField(verbose_name="project_id", name="project_id",
                             primary_key=True, unique=True, db_index=True)
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=6, unique=True)
    created_date = models.DateTimeField(null=False, blank=False,default=timezone.now)
    modified_date = models.DateTimeField(null=False, blank=False,default=timezone.now)
    project_owner = models.ForeignKey("users.Profile", on_delete=models.CASCADE, related_name="owner")
    members = models.ManyToManyField("users.Profile", related_name="members")
    documents = models.FileField()
    

