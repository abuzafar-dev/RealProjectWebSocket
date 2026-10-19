from django.contrib import admin

from chat.models import Message, Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', 'created_by', 'created_at']
    prepopulated_fields = {'slug': ['name']}


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'room', 'user', 'text', 'created_at']
    list_filter = ['room']
