# Generated by Django 3.1.5 on 2021-06-01 20:05

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0011_auto_20210601_1954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='time_added',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 1, 20, 5, 40, 293791, tzinfo=utc), max_length=64),
        ),
    ]