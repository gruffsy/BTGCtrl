# Generated by Django 2.2.7 on 2020-01-05 19:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('kontroll', '0040_avviktr_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='objtr',
            name='utbedret_avvik',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='utbedretavvik_avvik', to='kontroll.Avvik'),
        ),
    ]
