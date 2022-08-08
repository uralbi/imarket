from django.contrib import admin
from .models import Category


class CategroyAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('id','category_name', 'slug', 'description')


admin.site.register(Category, CategroyAdmin)