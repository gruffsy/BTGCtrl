# Generated by Django 2.2.7 on 2019-12-10 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kontroll', '0028_auto_20191210_1621'),
    ]

    operations = [
        migrations.AddField(
            model_name='month',
            name='intervall',
            field=models.PositiveSmallIntegerField(default=5),
        ),
    ]
