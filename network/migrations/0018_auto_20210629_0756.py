# Generated by Django 3.1.5 on 2021-06-29 07:56

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0017_auto_20210628_1410'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='time_added',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 29, 7, 56, 37, 66296, tzinfo=utc), max_length=64),
        ),
    ]
