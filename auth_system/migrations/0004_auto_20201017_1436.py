# Generated by Django 3.1.1 on 2020-10-17 14:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth_system', '0003_auto_20201012_1520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='last_password_change',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='Дата і час, коли було останній раз змінено пароль, якщо не мінявся, то дата створення', verbose_name='Част останньої зміни паролю'),
        ),
    ]
