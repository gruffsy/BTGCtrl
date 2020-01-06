# Generated by Django 2.2.7 on 2020-01-05 14:57

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):
    dependencies = [
        ('kontroll', '0037_auto_20200104_2257'),
    ]

    operations = [
        migrations.AddField(
            model_name='avvik',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 5, 14, 57, 32, 141489, tzinfo=utc),
                                       editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='avvik',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 5, 14, 57, 42, 140781, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='AvvikTr',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(editable=False)),
                ('modified', models.DateTimeField()),
                ('avvik', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kontroll.Avvik')),
                ('object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kontroll.Object')),
            ],
        ),
    ]
