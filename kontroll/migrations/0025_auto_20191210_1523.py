# Generated by Django 2.2.7 on 2019-12-10 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kontroll', '0024_auto_20191210_1522'),
    ]

    operations = [
        migrations.AddField(
            model_name='object',
            name='nestekontroll',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='object',
            name='nesteservice',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='object',
            name='sistekontroll',
            field=models.DateField(blank=True, null=True),
        ),
    ]