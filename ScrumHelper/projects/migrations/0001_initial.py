# Generated by Django 3.0.2 on 2020-03-02 15:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('project_id', models.IntegerField(db_index=True, primary_key=True, serialize=False, unique=True, verbose_name='project_id')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('code', models.CharField(max_length=6, unique=True)),
                ('documents', models.FileField(upload_to='')),
            ],
        ),
    ]
