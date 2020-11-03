# Generated by Django 3.1.1 on 2020-11-03 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0006_history'),
        ('auth_system', '0004_auto_20201017_1436'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='checked_news',
            field=models.ManyToManyField(related_name='users_saw', through='news.History', to='news.News'),
        ),
    ]
