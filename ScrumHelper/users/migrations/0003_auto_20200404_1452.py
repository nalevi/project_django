# Generated by Django 3.0.3 on 2020-04-04 12:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_profile_work_log'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='role',
            new_name='team',
        ),
    ]
