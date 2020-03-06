from django.db import models
from django.utils import timezone

from users.models import Profile

from projects.models import MetaStory

class UserStory(MetaStory):
    '''
    UserStory object's model. Inherited from MetaStory
    '''
    id = models.IntegerField(verbose_name="userstory_id", name="userstory_id",
                            primary_key=True, unique=True, db_index=True)
    #worklog = 