# Generated by Django 5.1.1 on 2024-11-04 19:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mailing',
            options={'ordering': ('-start_datetime',), 'permissions': [('can_deactivate_mailing', 'can deactivate mailing')], 'verbose_name': 'Рассылка', 'verbose_name_plural': 'Рассылки'},
        ),
    ]
