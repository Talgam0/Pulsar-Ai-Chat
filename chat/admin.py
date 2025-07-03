from django.contrib import admin
from .models import ChatSession, Message

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['user__username', 'title']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['session_user', 'message_type', 'content_preview', 'created_at']
    list_filter = ['message_type', 'created_at']
    search_fields = ['content', 'session__user__username']
    readonly_fields = ['created_at']
    
    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Содержание'
    
    def session_user(self, obj):
        return obj.session.user.username
    session_user.short_description = 'Пользователь'
    