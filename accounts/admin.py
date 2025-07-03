# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Админка для наших пользователей"""
    
    # Какие поля показывать в списке
    list_display = ('username', 'email', 'user_type', 'is_staff')
    
    # По каким полям можно фильтровать
    list_filter = ('user_type', 'is_staff', 'is_active')
    
    # Добавляем наши поля в форму редактирования
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {
            'fields': ('user_type', 'avatar', 'bio')
        }),
    )
    