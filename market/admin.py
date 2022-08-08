from django.contrib import admin
from .models import Item, ItemGallery, SavedItem
import admin_thumbnails
from django.utils.html import format_html


class SavedItemAdmin(admin.ModelAdmin):
    model = SavedItem
    list_display = ('user', 'item', 'created_at')


@admin_thumbnails.thumbnail('image')
class GalleryInLine(admin.TabularInline):
    model = ItemGallery
    extra = 1
    show_change_link = True


class GalleryAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="50" style="border-radius:10%;">'.format(object.image.url))

    thumbnail.short_description = 'Picture'
    list_display = ('id','thumbnail', 'image')


class ItemAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'status', 'price', 'description', 'category', 'modified_date', 'created_date')
    prepopulated_fields = {'slug': ('item_name',)}
    inlines = [GalleryInLine]


admin.site.register(Item, ItemAdmin)
admin.site.register(ItemGallery, GalleryAdmin)
admin.site.register(SavedItem, SavedItemAdmin)