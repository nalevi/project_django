# Generated by Django 3.0.2 on 2020-03-09 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='importance',
            field=models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='low', max_length=8),
        ),
        migrations.AlterField(
            model_name='issue',
            name='state',
            field=models.CharField(choices=[('OPEN', 'Open'), ('CLOSED', 'Closed'), ('IN PROGRESS', 'In Progress'), ('TESTING', 'Testing'), ('DONE', 'Done')], default='OPEN', max_length=15),
        ),
    ]