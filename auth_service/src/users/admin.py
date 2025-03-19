from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    # Поля, которые будут отображаться в списке пользователей
    list_display = ['username', 'email', 'phone', 'is_staff']

    # Поля в форме редактирования пользователя
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительные данные', {'fields': ('phone',)}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
