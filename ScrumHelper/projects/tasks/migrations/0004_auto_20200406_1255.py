# Generated by Django 3.0.3 on 2020-04-06 10:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_profile_avatar'),
        ('tasks', '0003_task_epic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='assignee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='task_assignee', to='users.Profile'),
        ),
    ]
