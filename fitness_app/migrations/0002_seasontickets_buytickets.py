# Generated by Django 5.0.3 on 2024-03-17 20:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitness_app', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SeasonTickets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена')),
                ('number_of_months', models.SmallIntegerField(verbose_name='Количество месяцев')),
            ],
            options={
                'verbose_name': 'Сезонный билет',
                'verbose_name_plural': 'Сезонные билеты',
                'ordering': ['-price'],
            },
        ),
        migrations.CreateModel(
            name='BuyTickets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField(auto_now_add=True, verbose_name='Начало')),
                ('end', models.DateTimeField(verbose_name='Конец')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to=settings.AUTH_USER_MODEL)),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_tickets', to='fitness_app.seasontickets')),
            ],
        ),
    ]
