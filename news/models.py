from django.db import models

from django.shortcuts import reverse
from django.utils.text import slugify


# Create your models here.


class Category(models.Model):
    name = models.CharField('Категорія', max_length=100, help_text='Категорія для новин')
    description = models.TextField('Опис', blank=True, help_text='Короткий опис категорії')
    slug = models.SlugField(max_length=160, unique=True,
                            help_text='Слаг для url, генерується сам із назви, але можна задат вручну',
                            blank=True)

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.name and not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
