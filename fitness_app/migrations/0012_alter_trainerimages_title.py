# Generated by Django 5.0.3 on 2024-03-19 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitness_app', '0011_alter_trainerimages_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trainerimages',
            name='title',
            field=models.CharField(blank=True, max_length=100, verbose_name='Заголовок'),
        ),
    ]
