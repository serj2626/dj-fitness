# Generated by Django 5.0.3 on 2024-03-22 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitness_app', '0022_ordertraining_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trainer',
            name='position',
            field=models.CharField(choices=[('fitness', 'Инструктор тренажерного зала'), ('pool', 'Инструктор бассейна'), ('yoga', 'Инструктор йоги'), ('groups', 'Тренер групповых тренировок')], max_length=100, verbose_name='Должность'),
        ),
    ]
