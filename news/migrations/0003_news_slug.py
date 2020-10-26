# Generated by Django 3.1.1 on 2020-10-26 11:54

from django.db import migrations, models
import news.utils


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_news'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='slug',
            field=models.SlugField(blank=True, default=news.utils.unique_slug, unique=True, verbose_name='Слаг'),
        ),
    ]
