# Generated by Django 3.0.3 on 2020-03-28 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0003_remove_comment_owner_usr'),
        ('worklogs', '0001_initial'),
        ('stories', '0010_auto_20200321_1853'),
    ]

    operations = [
        migrations.AddField(
            model_name='userstory',
            name='work_log',
            field=models.ManyToManyField(to='worklogs.Worklog'),
        ),
        migrations.AlterField(
            model_name='userstory',
            name='comment',
            field=models.ManyToManyField(related_name='userstory_comment', to='comments.Comment'),
        ),
    ]