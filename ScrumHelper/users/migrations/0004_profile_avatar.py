# Generated by Django 3.0.3 on 2020-04-04 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20200404_1452'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='avatars'),
        ),
    ]