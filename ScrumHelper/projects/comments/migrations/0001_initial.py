# Generated by Django 3.0.2 on 2020-03-21 16:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(null=True)),
                ('created_date', models.DateField(default=django.utils.timezone.now)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
