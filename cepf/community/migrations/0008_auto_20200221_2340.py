# Generated by Django 3.0.2 on 2020-02-21 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0007_auto_20200221_2332'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventtoschedule',
            name='recommendedDateTime',
        ),
        migrations.AlterField(
            model_name='eventtoschedule',
            name='recommendedTime',
            field=models.TimeField(default=None),
        ),
    ]
