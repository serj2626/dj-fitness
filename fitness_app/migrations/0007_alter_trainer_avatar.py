# Generated by Django 5.0.3 on 2024-03-19 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitness_app', '0006_buytickets_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trainer',
            name='avatar',
            field=models.ImageField(blank=True, default='trainers/trainer.jpg', upload_to='get_path_for_avatar_for_trainer', verbose_name='Аватар'),
        ),
    ]
