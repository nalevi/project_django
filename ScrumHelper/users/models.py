from django.db import models

# Create your models here.
class User(models.Model):
    uuid = models.IntegerField(primary_key=True, db_index=True,
                               auto_created=True,unique=True)
    username = models.CharField("username", max_length=255, unique=True,
        help_text="Required. 30 characters or fewer. Letters, numbers and "
                    "/./-/_ characters"
        )
    full_name = models.CharField("full name", max_length=256, blank=True)
    email = models.EmailField("email address", max_length=255, blank=True, unique=True)