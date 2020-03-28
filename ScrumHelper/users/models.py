from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from worklogs.models import Worklog

class Profile(models.Model):
    """
        A users profile. This extends the built-in User object.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=30, blank=True)
    #avatar = models.ImageField(upload_to='avatars')
    work_log = models.ManyToManyField("worklogs.Worklog")

    def __str__(self):
        return self.user.username

    def getFullName(self):
        return self.user.first_name + " " + self.user.last_name

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()