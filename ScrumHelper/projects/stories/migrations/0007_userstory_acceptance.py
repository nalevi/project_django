# Generated by Django 3.0.3 on 2020-03-18 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0006_auto_20200318_1512'),
    ]

    operations = [
        migrations.AddField(
            model_name='userstory',
            name='acceptance',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
