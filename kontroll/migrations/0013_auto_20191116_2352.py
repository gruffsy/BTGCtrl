# Generated by Django 2.2.7 on 2019-11-16 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kontroll', '0012_auto_20191116_2344'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='extinguishant',
            name='navn',
        ),
        migrations.AddField(
            model_name='extinguishant',
            name='slukkemiddel',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
