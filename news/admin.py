from django.contrib import admin

from .models import Category
from .models import News
from .models import History
# Register your models here.

admin.site.register(Category)
admin.site.register(News)


@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'news', 'checked_at', 'is_checked_on_site', 'is_checked_on_email',)

