# Generated by Django 3.0.2 on 2020-03-07 15:51

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0004_auto_20200307_1514'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Epic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Unkown', max_length=50, unique=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('description', models.CharField(default='Description', max_length=250)),
                ('assignee', models.ForeignKey(default='Unkown', on_delete=django.db.models.deletion.CASCADE, related_name='epic_assignee', to='users.Profile')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='epic_owner', to='users.Profile')),
                ('project_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='epic_project_code', to='projects.Project', to_field='code')),
            ],
        ),
    ]
