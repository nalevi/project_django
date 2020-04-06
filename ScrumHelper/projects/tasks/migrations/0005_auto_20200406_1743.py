# Generated by Django 3.0.3 on 2020-04-06 15:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('epics', '0002_remove_epic_assignee'),
        ('tasks', '0004_auto_20200406_1255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='epic',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='task_epic', to='epics.Epic'),
        ),
    ]
