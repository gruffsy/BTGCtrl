# Generated by Django 2.2.7 on 2020-01-24 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kontroll', '0044_objtr_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='object',
            name='status',
            field=models.PositiveSmallIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='objtr',
            name='status',
            field=models.PositiveSmallIntegerField(default=1),
        ),
    ]