# Generated by Django 2.2.7 on 2020-01-04 10:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('kontroll', '0034_delete_avviktr'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='kommentar',
            new_name='gml_id',
        ),
        migrations.AddField(
            model_name='object',
            name='gml_kid',
            field=models.TextField(blank=True, null=True),
        ),
    ]
