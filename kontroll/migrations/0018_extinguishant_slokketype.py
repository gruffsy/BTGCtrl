# Generated by Django 2.2.7 on 2019-11-21 17:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('kontroll', '0017_auto_20191121_1855'),
    ]

    operations = [
        migrations.AddField(
            model_name='extinguishant',
            name='slokketype',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='kontroll.Slokketype'),
            preserve_default=False,
        ),
    ]