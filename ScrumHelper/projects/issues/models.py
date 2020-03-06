from django.db import models
from django.utils import timezone

from users.models import Profile

from projects.models import MetaStory

class Issue(MetaStory):
    '''
    Issue object's model. Inherited from MetaStory
    '''
    id = models.IntegerField(verbose_name="issue_id", name="issue_id",
                            primary_key=True, unique=True, db_index=True)
    #worklog = 
    defect_type = models.CharField(max_length=10)
    solved = models.BooleanField(default=False)
    solution = models.CharField(max_length=150)
