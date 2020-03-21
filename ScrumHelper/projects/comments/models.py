from django.db import models
from django.utils import timezone

from users.models import Profile

class Comment(models.Model):
    '''
    Comment object
    '''
    text = models.TextField(null=True)
    created_date = models.DateField(default=timezone.now, null=False,blank=False)
    owner = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="comment_owner")

