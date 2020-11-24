from django.contrib import admin

from .models import User, Review
# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass