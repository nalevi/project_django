from django.db import models
from django.utils import timezone

from users.models import Profile

from projects.models import MetaStory

class Task(MetaStory):
    '''
     Task object's model, inherited from MetaStory.
    '''
    id = models.IntegerField(verbose_name="task_id", name="task_id",
                            primary_key=True, unique=True, db_index=True)

    