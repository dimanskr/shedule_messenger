# Generated by Django 5.1.1 on 2024-10-11 18:53

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mailingattempt',
            options={'ordering': ('-last_attempt', 'status'), 'verbose_name': 'Попытка рассылки', 'verbose_name_plural': 'Попытки рассылок'},
        ),
        migrations.RenameField(
            model_name='mailing',
            old_name='client',
            new_name='clients',
        ),
        migrations.AlterField(
            model_name='mailing',
            name='periodicity',
            field=models.CharField(choices=[('once', 'Однократная'), ('daily', 'Ежедневная'), ('weekly', 'Еженедельная'), ('monthly', 'Ежемесячная')], default='once', max_length=10),
        ),
        migrations.AlterField(
            model_name='mailing',
            name='start_datetime',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата и время отправки рассылки'),
        ),
        migrations.AlterField(
            model_name='mailing',
            name='status',
            field=models.CharField(choices=[('created', 'Создана'), ('started', 'Запущена'), ('completed', 'Завершена')], default='created', max_length=10),
        ),
        migrations.AlterField(
            model_name='mailingattempt',
            name='last_attempt',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата и время попытки'),
        ),
        migrations.AlterField(
            model_name='mailingattempt',
            name='mailing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attempts', to='mailing.mailing', verbose_name='Попытка рассылки'),
        ),
        migrations.AlterField(
            model_name='mailingattempt',
            name='status',
            field=models.CharField(choices=[('success', 'успешно'), ('failed', 'не успешно')], verbose_name='Статус отправки'),
        ),
    ]
