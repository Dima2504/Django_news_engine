# Generated by Django 3.1.1 on 2020-10-11 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Категорія для новин', max_length=100, verbose_name='Категорія')),
                ('description', models.TextField(blank=True, help_text='Короткий опис категорії', verbose_name='Опис')),
                ('slug', models.SlugField(blank=True, help_text='Слаг для url, генерується сам із назви, але можна задат вручну', max_length=160, unique=True)),
            ],
            options={
                'verbose_name': 'Категорія',
                'verbose_name_plural': 'Категорії',
            },
        ),
    ]
