# Generated by Django 3.1.1 on 2020-10-27 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_news_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='source_name',
            field=models.CharField(max_length=200, verbose_name='Назва ресурсу'),
        ),
    ]
