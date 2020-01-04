# Generated by Django 2.2.7 on 2020-01-04 21:57

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):
    dependencies = [
        ('kontroll', '0036_auto_20200104_2254'),
    ]

    operations = [
        migrations.AddField(
            model_name='object',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 4, 21, 57, 3, 167846, tzinfo=utc),
                                       editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='object',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 4, 21, 57, 16, 955774, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='objtr',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 4, 21, 57, 29, 182440, tzinfo=utc),
                                       editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='objtr',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 4, 21, 57, 39, 448220, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
