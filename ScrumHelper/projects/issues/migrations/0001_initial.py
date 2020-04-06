# Generated by Django 3.0.2 on 2020-03-08 19:16

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Unkown', max_length=50, unique=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('description', models.CharField(default='Description', max_length=250)),
                ('importance', models.CharField(default='Low', max_length=8)),
                ('state', models.CharField(default='OPEN', max_length=15)),
                ('defect_type', models.CharField(max_length=10)),
                ('solved', models.BooleanField(default=False)),
                ('solution', models.CharField(max_length=150)),
                ('assignee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='issue_assignee', to='users.Profile')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issue_owner', to='users.Profile')),
                ('project_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issue_project_code', to='projects.Project', to_field='code')),
            ],
        ),
    ]
