from django.contrib import admin
from .models import Chat

class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'subject', 'content', 'created_at', 'is_read')

admin.site.register(Chat, ChatAdmin)