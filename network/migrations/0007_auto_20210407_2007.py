# Generated by Django 3.1.5 on 2021-04-07 20:07

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0006_auto_20210405_1947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follow',
            name='followee',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='followee', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='follow',
            name='follower',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='follower', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='time_added',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 7, 20, 7, 35, 197894, tzinfo=utc), max_length=64),
        ),
    ]