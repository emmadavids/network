# Generated by Django 3.1.5 on 2021-04-05 19:47

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_auto_20210403_2004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='time_added',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 5, 19, 47, 42, 562709, tzinfo=utc), max_length=64),
        ),
    ]