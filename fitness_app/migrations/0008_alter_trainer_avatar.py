# Generated by Django 5.0.3 on 2024-03-19 19:26

import fitness_app.service
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitness_app', '0007_alter_trainer_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trainer',
            name='avatar',
            field=models.ImageField(blank=True, default='trainers/trainer.jpg', upload_to=fitness_app.service.get_path_for_avatar_for_trainer, verbose_name='Аватар'),
        ),
    ]
