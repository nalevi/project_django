from django.db import models

from users.models import Profile

class Project(models.Model):
    """
        Project object's model class.
    """
    id = models.IntegerField(verbose_name="project_id", name="project_id",
                             primary_key=True, unique=True, db_index=True)
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=6, unique=True)
    created_date = models.DateField()
    project_owner = models.ForeignKey("users.Profile", on_delete=models.CASCADE)
    documents = models.FileField()

