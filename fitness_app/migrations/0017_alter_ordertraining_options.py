# Generated by Django 5.0.3 on 2024-03-20 20:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fitness_app', '0016_rate_count_minutes_ordertraining'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ordertraining',
            options={'verbose_name': 'Купленное занятие', 'verbose_name_plural': 'Купленные занятия'},
        ),
    ]
