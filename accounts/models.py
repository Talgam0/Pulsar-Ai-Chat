# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Наш пользователь - может быть родителем, специалистом и т.д."""
    
    # Типы пользователей
    USER_TYPES = (
        ('parent', 'Родитель'),
        ('specialist', 'Специалист'),
        ('person_with_autism', 'Человек с РАС'),
        ('caregiver', 'Опекун'),
    )
    
    # Дополнительные поля
    user_type = models.CharField(
        max_length=20, 
        choices=USER_TYPES, 
        default='parent',
        verbose_name='Тип пользователя'
    )
    
    avatar = models.ImageField(
        upload_to='avatars/', 
        null=True, 
        blank=True,
        verbose_name='Фото профиля'
    )
    
    bio = models.TextField(
        max_length=500, 
        blank=True,
        verbose_name='О себе'
    )
    
    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"
