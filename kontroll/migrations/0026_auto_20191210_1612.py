# Generated by Django 2.2.7 on 2019-12-10 15:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kontroll', '0025_auto_20191210_1523'),
    ]

    operations = [
        migrations.AlterField(
            model_name='object',
            name='nesteservice',
            field=models.DateField(blank=True, default=datetime.datetime(2010, 12, 10, 0, 0)),
        ),
    ]