# Generated by Django 3.0.3 on 2020-04-06 10:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stories', '0011_auto_20200328_1814'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userstory',
            name='assignee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='userstory_assignee', to=settings.AUTH_USER_MODEL),
        ),
    ]
