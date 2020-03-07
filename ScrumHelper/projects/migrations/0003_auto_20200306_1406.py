# Generated by Django 3.0.2 on 2020-03-06 13:06

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('projects', '0002_auto_20200303_1937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='project_owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_owner', to='users.Profile'),
        ),
    ]
