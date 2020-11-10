from django.db import models

from django.db.models.signals import post_delete
from django.dispatch import receiver

from django_celery_beat.models import PeriodicTask, IntervalSchedule

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import UserManager

from django.core.mail import send_mail

from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
import datetime
import json

from news.models import Category
from news.models import News
from news.models import History


class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        _('email address'),
        unique=True,
        error_messages={
            'unique': _("A user with that email already exists."),
        }
    )
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    categories = models.ManyToManyField(Category, related_name='users',
                                        help_text='Категорії, які користувач відслідковує', blank=True)

    last_password_change = models.DateTimeField('Част останньої зміни паролю',
                                                help_text='Дата і час, коли було останній раз змінено пароль, якщо не мінявся, то дата створення',
                                                default=timezone.now)
    checked_news = models.ManyToManyField(News, through=History, related_name='users_saw')

    email_periodic_task = models.OneToOneField(PeriodicTask, verbose_name="Зв'язана задача по відправці новин на пошту",
                                               on_delete=models.SET_NULL, null=True, blank=True)

    _send_news_to_email = models.BooleanField('Надсилати новини на пошту',
                                              help_text='Активуйте, якщо хочете отримувати новини на пошту',
                                              default=False)

    _countdown_to_email = models.DurationField(verbose_name='Відрізок часу між відправкою новин на пошту',
                                               help_text='Найменший період між відправленнями новин на пошту',
                                               default=datetime.timedelta(minutes=60))

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def set_password(self, *args, **kwargs):
        super().set_password(*args, **kwargs)
        self.last_password_change = timezone.now()
        self.save()

    def _get_or_create_interval(self):
        return IntervalSchedule.objects.get_or_create(every=self._countdown_to_email.seconds / 60,
                                                      period=IntervalSchedule.MINUTES)

    def _set_or_create_periodic_task(self, enabled=True):
        if not self.email_periodic_task:
            interval, _ = self._get_or_create_interval()
            self.email_periodic_task = PeriodicTask.objects.create(interval=interval, name=f'"{self.email}" PT',
                                                                   task='news.tasks.send_one_news_to_one_user_task',
                                                                   args=json.dumps([self.id]), enabled=enabled)
        else:
            self.email_periodic_task.enabled = enabled
            self.email_periodic_task.save()

    send_news_to_email = property()
    countdown_to_email = property()

    @send_news_to_email.getter
    def send_news_to_email(self):
        return self._send_news_to_email

    @send_news_to_email.setter
    def send_news_to_email(self, is_send):
        self._send_news_to_email = is_send
        self._set_or_create_periodic_task(enabled=is_send)

    @countdown_to_email.getter
    def countdown_to_email(self):
        return self._countdown_to_email

    @countdown_to_email.setter
    def countdown_to_email(self, timedelta):
        self._countdown_to_email = timedelta
        if self.email_periodic_task:
            self.email_periodic_task.interval, _ = self._get_or_create_interval()
            self.email_periodic_task.save()

    def __str__(self):
        return self.email


@receiver(post_delete, sender=User)
def delete_user_email_task(sender, instance, using, **kwargs):
    if instance.email_periodic_task:
        temp = instance.email_periodic_task
        temp.delete()
