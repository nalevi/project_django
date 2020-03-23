from django.db import models
from django.utils import timezone

from users.models import Profile

def project_directory_path(instance, filename):
    return 'documents/{0}'.format(filename)

class Project(models.Model):
    """
        Project object's model class.
    """
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=6, unique=True)
    created_date = models.DateTimeField(null=False, blank=False,default=timezone.now)
    modified_date = models.DateTimeField(null=False, blank=False,default=timezone.now)
    project_owner = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="project_owner")
    release = models.CharField(max_length=10, null=True)
    documents = models.ManyToManyField("projects.Documents")

    def __str__(self):
        return self.code


class Documents(models.Model):
    """
        Project documents' model class
    """
    document = models.FileField(upload_to=project_directory_path)

    def __str__(self):
        return self.document.name.split('/')[1]