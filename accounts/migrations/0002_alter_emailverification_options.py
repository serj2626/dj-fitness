# Generated by Django 5.0.3 on 2024-03-18 16:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='emailverification',
            options={'verbose_name': 'Верификация почты', 'verbose_name_plural': 'Верификация почты'},
        ),
    ]
