# Generated by Django 5.0.3 on 2024-03-19 21:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitness_app', '0008_alter_trainer_avatar'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderTicket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField(auto_now_add=True, verbose_name='Начало')),
                ('end', models.DateTimeField(verbose_name='Конец')),
                ('status', models.BooleanField(default=False, verbose_name='Оплачен')),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_tickets', to='fitness_app.seasontickets')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Купленный абонемент',
                'verbose_name_plural': 'Купленные абонементы',
            },
        ),
        migrations.DeleteModel(
            name='BuyTickets',
        ),
    ]
