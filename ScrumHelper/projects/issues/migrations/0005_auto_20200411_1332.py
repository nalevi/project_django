# Generated by Django 3.0.5 on 2020-04-11 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0004_auto_20200411_1322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='defect_type',
            field=models.CharField(max_length=25),
        ),
    ]
