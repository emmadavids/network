# Generated by Django 3.1.5 on 2021-06-29 09:00

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0018_auto_20210629_0756'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='time_added',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 29, 9, 0, 42, 40151, tzinfo=utc), max_length=64),
        ),
    ]
