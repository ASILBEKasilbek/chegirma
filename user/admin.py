from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom User admin panel"""
    list_display = ['telefon', 'email', 'ism', 'familiya', 'is_staff', 'yaratilgan_vaqt']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'yaratilgan_vaqt']
    search_fields = ['telefon', 'email', 'ism', 'familiya']
    ordering = ['-yaratilgan_vaqt']
    
    fieldsets = (
        (None, {'fields': ('telefon', 'password')}),
        (_('Shaxsiy ma\'lumotlar'), {'fields': ('ism', 'familiya', 'email', 'rasm')}),
        (_('Ruxsatlar'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Muhim sanalar'), {'fields': ('last_login', 'yaratilgan_vaqt')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('telefon', 'email', 'ism', 'familiya', 'password1', 'password2'),
        }),
    )
    
    readonly_fields = ['yaratilgan_vaqt', 'last_login']

