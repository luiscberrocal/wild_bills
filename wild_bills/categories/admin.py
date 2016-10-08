from django.contrib import admin

# Register your models here.
from parler.admin import TranslatableAdmin

from .models import Category

class CategoryAdmin(TranslatableAdmin):
    list_display = ('name', 'owner', 'slug', 'is_public')

admin.site.register(Category, CategoryAdmin)