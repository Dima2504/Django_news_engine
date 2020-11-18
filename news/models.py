from django.db import models
from django.utils.text import slugify
from .utils import unique_slug
from django.conf import settings

# Create your models here.


class Category(models.Model):
    name = models.CharField('Категорія', max_length=100, help_text='Категорія для новин')
    description = models.TextField('Опис', blank=True, help_text='Короткий опис категорії')
    slug = models.SlugField(max_length=160, unique=True,
                            help_text='Слаг для url, генерується сам із назви, але можна задат вручну',
                            blank=True)
    is_main = models.BooleanField('Чи головна категорія',
                                  help_text='Головні категорії відображаються на початковій сторінці та є обов\'язковими',
                                  default=False)

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
    source_name = models.CharField(max_length=200, verbose_name='Назва ресурсу')
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


class History(models.Model):
    ON_SITE = 'site'
    ON_EMAIL = 'email'
    ON_TELEGRAM = 'telegram'
    ON_APP = 'app'
    CHECKED_CHOICES = [
        (ON_SITE, 'На сайті'),
        (ON_EMAIL, 'На пошті'),
        (ON_TELEGRAM, 'В телеграмі'),
        (ON_APP, 'У мобільній програмі'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    checked_at = models.DateTimeField(verbose_name='Дата і час перегляду новини', auto_now_add=True)
    checked_on = models.CharField(max_length=8, choices=CHECKED_CHOICES, default=ON_SITE, verbose_name='Переглянуто на ', help_text='Де користувач переглянув дану новину')

    class Meta:
        verbose_name = 'Історія перегляду новин'
        verbose_name_plural = 'Історії перегляду новин'

    def __str__(self):
        return 'Новина "{}" була пегелянута користувачем "{}" в: {}'.format(self.news, self.user, self.checked_at.ctime())