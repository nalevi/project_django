# Generated by Django 3.0.2 on 2020-03-23 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='members',
        ),
        migrations.AddField(
            model_name='project',
            name='release',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
