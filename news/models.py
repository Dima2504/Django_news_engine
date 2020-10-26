from django.db import models
import time
from django.shortcuts import reverse
from django.utils.text import slugify
from .utils import unique_slug

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
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class News(models.Model):
    category = models.ForeignKey(Category, related_name='news', on_delete=models.CASCADE)
    author = models.CharField(max_length=130, verbose_name='Автор')
    title = models.CharField(max_length=400, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Опис', help_text='Короткий фрагмент')
    url = models.URLField(verbose_name='Посилання на ресурс', max_length=400)
    url_to_image = models.URLField(verbose_name='Посилання на картинку', max_length=400)
    published_at = models.DateTimeField('Дата публікації')
    content = models.TextField(verbose_name='Контент')
    slug = models.SlugField(verbose_name='Слаг', blank=True, unique=True, default=unique_slug)

    class Meta:
        verbose_name = 'Новина'
        verbose_name_plural = 'Новини'
        ordering = ['-published_at', ]
        unique_together = (('title', 'published_at'),)

    def __repr__(self):
        return self.title
    def __str__(self):
        return self.title
